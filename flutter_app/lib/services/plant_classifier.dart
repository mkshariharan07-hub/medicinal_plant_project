import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/services.dart';
import 'package:image/image.dart' as img;
import 'package:tflite_flutter/tflite_flutter.dart';
import 'dart:convert';
import '../models/plant_model.dart';

class PlantClassifier {
  Interpreter? _interpreter;
  List<String>? _labels;
  Map<String, MedicinalPlant>? _plantDatabase;
  bool _isInitialized = false;

  static const int INPUT_SIZE = 224;
  static const int NUM_CLASSES = 100;

  Future<void> initialize() async {
    if (_isInitialized) return;

    try {
      // Load TFLite model
      final interpreterOptions = InterpreterOptions()..threads = 4;
      _interpreter = await Interpreter.fromAsset(
        'assets/model/medicinal_plant_model.tflite',
        options: interpreterOptions,
      );

      print('Model loaded successfully');

      // Load class labels
      final labelsData = await rootBundle.loadString('assets/model/class_indices.json');
      final labelsJson = json.decode(labelsData) as Map<String, dynamic>;
      _labels = labelsJson.values.map((e) => e.toString()).toList();

      print('Labels loaded: ${_labels?.length} classes');

      // Load plant database
      final databaseData = await rootBundle.loadString('assets/medicinal_plants_database.json');
      final databaseJson = json.decode(databaseData);
      final plantsList = (databaseJson['medicinal_plants_database'] as List)
          .map((e) => MedicinalPlant.fromJson(e))
          .toList();

      _plantDatabase = {
        for (var plant in plantsList) plant.name: plant,
      };

      print('Plant database loaded: ${_plantDatabase?.length} plants');

      _isInitialized = true;
    } catch (e) {
      print('Error initializing classifier: $e');
      rethrow;
    }
  }

  Future<List<PredictionResult>> predict(String imagePath) async {
    if (!_isInitialized) {
      await initialize();
    }

    try {
      // Load and preprocess image
      final imageData = await _preprocessImage(imagePath);

      // Prepare input and output tensors
      var input = imageData.reshape([1, INPUT_SIZE, INPUT_SIZE, 3]);
      var output = List.filled(1 * NUM_CLASSES, 0.0).reshape([1, NUM_CLASSES]);

      // Run inference
      _interpreter!.run(input, output);

      // Get predictions
      final predictions = output[0] as List<double>;

      // Get top 5 predictions
      final results = _getTopPredictions(predictions, topK: 5);

      return results;
    } catch (e) {
      print('Error during prediction: $e');
      rethrow;
    }
  }

  Future<Float32List> _preprocessImage(String imagePath) async {
    // Read image file
    final imageFile = File(imagePath);
    final imageBytes = await imageFile.readAsBytes();

    // Decode image
    img.Image? image = img.decodeImage(imageBytes);
    if (image == null) {
      throw Exception('Failed to decode image');
    }

    // Resize image to model input size
    final resized = img.copyResize(
      image,
      width: INPUT_SIZE,
      height: INPUT_SIZE,
      interpolation: img.Interpolation.cubic,
    );

    // Convert to Float32List and normalize [0, 1]
    final convertedBytes = Float32List(1 * INPUT_SIZE * INPUT_SIZE * 3);
    var buffer = 0;

    for (var y = 0; y < INPUT_SIZE; y++) {
      for (var x = 0; x < INPUT_SIZE; x++) {
        final pixel = resized.getPixel(x, y);
        convertedBytes[buffer++] = img.getRed(pixel) / 255.0;
        convertedBytes[buffer++] = img.getGreen(pixel) / 255.0;
        convertedBytes[buffer++] = img.getBlue(pixel) / 255.0;
      }
    }

    return convertedBytes;
  }

  List<PredictionResult> _getTopPredictions(List<double> predictions, {int topK = 5}) {
    // Create list of (index, probability) pairs
    final indexed = <MapEntry<int, double>>[];
    for (var i = 0; i < predictions.length; i++) {
      indexed.add(MapEntry(i, predictions[i]));
    }

    // Sort by probability (descending)
    indexed.sort((a, b) => b.value.compareTo(a.value));

    // Get top K results
    final results = <PredictionResult>[];
    for (var i = 0; i < topK && i < indexed.length; i++) {
      final entry = indexed[i];
      final plantName = _labels?[entry.key] ?? 'Unknown';
      final confidence = entry.value;

      final plantDetails = _plantDatabase?[plantName];

      results.add(PredictionResult(
        plantName: plantName,
        confidence: confidence,
        plantDetails: plantDetails,
        timestamp: DateTime.now(),
      ));
    }

    return results;
  }

  MedicinalPlant? getPlantDetails(String plantName) {
    return _plantDatabase?[plantName];
  }

  List<MedicinalPlant> getAllPlants() {
    return _plantDatabase?.values.toList() ?? [];
  }

  void dispose() {
    _interpreter?.close();
    _isInitialized = false;
  }
}
