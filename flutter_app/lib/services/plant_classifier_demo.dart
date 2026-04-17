import 'dart:io';
import 'dart:typed_data';
import 'dart:convert';
import 'package:flutter/services.dart';
import '../models/plant_model.dart';

class PlantClassifierDemo {
  Map<String, MedicinalPlant>? _plantDatabase;
  bool _isInitialized = false;

  Future<void> initialize() async {
    if (_isInitialized) return;

    try {
      // Load plant database
      final databaseData = await rootBundle.loadString('assets/medicinal_plants_database.json');
      final databaseJson = json.decode(databaseData);
      final plantsList = (databaseJson['medicinal_plants_database'] as List)
          .map((e) => MedicinalPlant.fromJson(e))
          .toList();

      _plantDatabase = {
        for (var plant in plantsList) plant.name: plant,
      };

      print('Demo mode: Plant database loaded: ${_plantDatabase?.length} plants');

      _isInitialized = true;
    } catch (e) {
      print('Error initializing demo classifier: $e');
      rethrow;
    }
  }

  Future<List<PredictionResult>> predict(String imagePath) async {
    if (!_isInitialized) {
      await initialize();
    }

    // DEMO MODE: Return mock predictions
    // In real app, this would use the ML model
    
    // Simulate processing delay
    await Future.delayed(Duration(seconds: 1));

    // Get random plants for demo
    final plants = _plantDatabase!.values.toList();
    
    // Return top 5 predictions with mock confidence scores
    final results = <PredictionResult>[];
    
    // Top prediction
    results.add(PredictionResult(
      plantName: plants[0].name,
      confidence: 0.92,
      plantDetails: plants[0],
      timestamp: DateTime.now(),
      imagePath: imagePath,
    ));
    
    // Other predictions
    for (int i = 1; i < 5 && i < plants.length; i++) {
      results.add(PredictionResult(
        plantName: plants[i].name,
        confidence: 0.85 - (i * 0.15),
        plantDetails: plants[i],
        timestamp: DateTime.now(),
        imagePath: imagePath,
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
    _isInitialized = false;
  }
}
