import 'package:flutter/foundation.dart';
import '../models/plant_model.dart';
import '../services/plant_classifier_demo.dart';

class PlantProvider extends ChangeNotifier {
  final PlantClassifierDemo _classifier = PlantClassifierDemo();
  List<PredictionResult> _history = [];
  bool _isLoading = false;
  String? _error;

  List<PredictionResult> get history => _history;
  bool get isLoading => _isLoading;
  String? get error => _error;

  Future<void> initialize() async {
    try {
      await _classifier.initialize();
    } catch (e) {
      _error = e.toString();
      notifyListeners();
    }
  }

  Future<List<PredictionResult>> classifyImage(String imagePath) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final results = await _classifier.predict(imagePath);
      
      // Add to history with image path
      final resultWithImage = PredictionResult(
        plantName: results.first.plantName,
        confidence: results.first.confidence,
        plantDetails: results.first.plantDetails,
        timestamp: results.first.timestamp,
        imagePath: imagePath,
      );
      
      _history.insert(0, resultWithImage);
      
      _isLoading = false;
      notifyListeners();
      return results;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      rethrow;
    }
  }

  List<MedicinalPlant> getAllPlants() {
    return _classifier.getAllPlants();
  }

  @override
  void dispose() {
    _classifier.dispose();
    super.dispose();
  }
}
