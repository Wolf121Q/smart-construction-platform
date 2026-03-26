class ComplaintLocalModel {
  final String statusId;
  final String categoryId;
  final String subcategoryId;
  final String areaId;
  final String description;
  final String latitude;
  final String longitude;
  final String attachments;

  ComplaintLocalModel({
    required this.statusId,
    required this.categoryId,
    required this.subcategoryId,
    required this.areaId,
    required this.description,
    required this.latitude,
    required this.longitude,
    required this.attachments,
  });

  // Creating a method to convert the ComplaintLocalModel object to a Map<String, dynamic>.
  Map<String, dynamic> toMap() {
    return {
      'status_id': statusId,
      'category_id': categoryId,
      'subcategory_id': subcategoryId,
      'area_id': areaId,
      'description': description,
      'latitude': latitude,
      'longitude': longitude,
      'attachments': attachments,
    };
  }

  // Factory constructor to create a ComplaintLocalModel object from a Map<String, dynamic>.
  factory ComplaintLocalModel.fromMap(Map<String, dynamic> map) {
    return ComplaintLocalModel(
      statusId: map['status_id'] ?? '',
      categoryId: map['category_id'] ?? '',
      subcategoryId: map['subcategory_id'] ?? '',
      areaId: map['area_id'] ?? '',
      description: map['description'] ?? '',
      latitude: map['latitude'] ?? '',
      longitude: map['longitude'] ?? '',
      attachments: map['attachments'] ?? '',
    );
  }
}
