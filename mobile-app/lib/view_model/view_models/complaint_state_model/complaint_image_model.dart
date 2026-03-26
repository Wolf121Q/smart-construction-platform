class ComplaintImageModel {
  final int status;
  final String message;
  final List<ImageDataArray> dataArray;

  ComplaintImageModel({
    required this.status,
    required this.message,
    required this.dataArray,
  });

  factory ComplaintImageModel.fromJson(Map<String, dynamic> json) {
    List<ImageDataArray> dataArray = (json['data_array'] as List)
        .map((data) => ImageDataArray.fromJson(data))
        .toList();

    return ComplaintImageModel(
      status: json['status'],
      // status: int.parse(json['status']),
      message: json['message'],
      dataArray: dataArray,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'status': status,
      'message': message,
      'data_array': dataArray.map((data) => data.toJson()).toList(),
    };
  }
}

class ImageDataArray {
  final String id;
  final String image;
  final String createdOn;
  final String updatedOn;
  final String ip;
  final String filename;
  final String attachment;
  final String latitude;
  final String longitude;
  final String createdBy;
  final String? updatedBy;
  final String? parent;
  final String? type;
  final int? status;
  final String complaint;
  final String complaintAction;
  final String complaintActionComment;

  ImageDataArray({
    required this.id,
    required this.image,
    required this.createdOn,
    required this.updatedOn,
    required this.ip,
    required this.filename,
    required this.attachment,
    required this.latitude,
    required this.longitude,
    required this.createdBy,
    this.updatedBy,
    this.parent,
    this.type,
    this.status,
    required this.complaint,
    required this.complaintAction,
    required this.complaintActionComment,
  });

  factory ImageDataArray.fromJson(Map<String, dynamic> json) {
    return ImageDataArray(
      id: json['id'] ?? "",
      image: json['image'] ?? "",
      createdOn: json['created_on'] ?? "",
      updatedOn: json['updated_on'] ?? "",
      ip: json['ip'] ?? "",
      filename: json['filename'] ?? "",
      attachment: json['attachment'] ?? "",
      latitude: json['latitude'] ?? "",
      longitude: json['longitude'] ?? "",
      createdBy: json['created_by'] ?? "",
      updatedBy: json['updated_by'] ?? "",
      parent: json['parent'] ?? "",
      type: json['type'] ?? "",
      // status: int.parse(json['status']),
      status: json['status'] ?? 0,
      complaint: json['complaint'] ?? "",
      complaintAction: json['complaint_action'] ?? "",
      complaintActionComment: json['complaint_action_comment'] ?? "",
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'image': image,
      'created_on': createdOn,
      'updated_on': updatedOn,
      'ip': ip,
      'filename': filename,
      'attachment': attachment,
      'latitude': latitude,
      'longitude': longitude,
      'created_by': createdBy,
      'updated_by': updatedBy,
      'parent': parent,
      'type': type,
      'status': status,
      'complaint': complaint,
      'complaint_action': complaintAction,
      'complaint_action_comment': complaintActionComment,
    };
  }
}
