class MedicinalPlant {
  final int id;
  final String name;
  final String scientificName;
  final Map<String, String> localNames;
  final List<String> uses;
  final String preparation;
  final String dosage;
  final String precautions;

  MedicinalPlant({
    required this.id,
    required this.name,
    required this.scientificName,
    required this.localNames,
    required this.uses,
    required this.preparation,
    required this.dosage,
    required this.precautions,
  });

  factory MedicinalPlant.fromJson(Map<String, dynamic> json) {
    return MedicinalPlant(
      id: json['id'] as int,
      name: json['name'] as String,
      scientificName: json['scientific_name'] as String,
      localNames: Map<String, String>.from(json['local_names']),
      uses: List<String>.from(json['uses']),
      preparation: json['preparation'] as String,
      dosage: json['dosage'] as String,
      precautions: json['precautions'] as String,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'scientific_name': scientificName,
      'local_names': localNames,
      'uses': uses,
      'preparation': preparation,
      'dosage': dosage,
      'precautions': precautions,
    };
  }
}

class PredictionResult {
  final String plantName;
  final double confidence;
  final MedicinalPlant? plantDetails;
  final DateTime timestamp;
  final String? imagePath;

  PredictionResult({
    required this.plantName,
    required this.confidence,
    this.plantDetails,
    required this.timestamp,
    this.imagePath,
  });

  Map<String, dynamic> toJson() {
    return {
      'plant_name': plantName,
      'confidence': confidence,
      'timestamp': timestamp.toIso8601String(),
      'image_path': imagePath,
    };
  }

  factory PredictionResult.fromJson(Map<String, dynamic> json) {
    return PredictionResult(
      plantName: json['plant_name'] as String,
      confidence: json['confidence'] as double,
      timestamp: DateTime.parse(json['timestamp'] as String),
      imagePath: json['image_path'] as String?,
    );
  }
}
