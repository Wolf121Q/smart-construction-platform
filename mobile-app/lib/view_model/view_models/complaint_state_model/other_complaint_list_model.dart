class OtherComplaintListDetailModel {
  final int status;

  final String message;
  final List<OtherComplaintItemModel> dataArray;

  OtherComplaintListDetailModel({
    required this.status,
    
    required this.message,
    required this.dataArray,
  });

  factory OtherComplaintListDetailModel.fromJson(Map<String, dynamic> json) {
    List<dynamic> data = json['data_array'];
    List<OtherComplaintItemModel> dataArray =
        data.map((item) => OtherComplaintItemModel.fromJson(item)).toList();

    return OtherComplaintListDetailModel(
      status: json['status'],
     // userId: json['user_id'],
      message: json['message'],
      dataArray: dataArray,
    );
  }
}

class OtherComplaintItemModel {
  final String uid;
  final String createdOn;
  final String updatedOn;
  final String createdBy;
  final String latitude;
  final String longitude;
  final String ip;
  final String serialNumber;
  final String status;
  final String area;
  final String category;
  final String subcategory;
  final String color;
  final String description;
  final double progress;

  OtherComplaintItemModel({
    required this.uid,
    required this.createdOn,
    required this.updatedOn,
    required this.createdBy,
    required this.latitude,
    required this.longitude,
    required this.ip,
    required this.serialNumber,
    required this.status,
    required this.area,
    required this.category,
    required this.subcategory,
    required this.color,
    required this.description,
    required this.progress,
  });

  factory OtherComplaintItemModel.fromJson(Map<String, dynamic> json) {
    return OtherComplaintItemModel(
      uid: json['uid'],
      createdOn: json['created_on'],
      updatedOn: json['updated_on'],
      createdBy: json['created_by'],
      latitude: json['latitude'] ?? "",
      longitude: json['longitude'] ?? "",
      ip: json['ip'],
      serialNumber: json['serial_number'],
      status: json['status'],
      area: json['area'],
      category: json['category'],
      subcategory: json['subcategory'],
      color: json['color'],
      description: json['description'],
      progress: json['progress'].toDouble(),
    );
  }



  Map<String, dynamic> toJson() {
    return {
      'uid': uid,
      'created_on': createdOn,
      'updated_on': updatedOn,
      'created_by': createdBy,
      'latitude': latitude,
      'longitude': longitude,
      'ip': ip,
      'serial_number': serialNumber,
      'status': status,
      'area': area,
      'category': category,
      'subcategory': subcategory,
      'color': color,
      'description': description,
      'progress': progress,
    };
  }

}
