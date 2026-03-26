class ComplaintDetailModel {
  final int status;
  final String message;
  final DataArray dataArray;

  ComplaintDetailModel({
    required this.status,
    required this.message,
    required this.dataArray,
  });

  factory ComplaintDetailModel.fromJson(Map<String, dynamic> json) {
    return ComplaintDetailModel(
      status: json['status'],
      message: json['message'],
      dataArray: DataArray.fromJson(json['data_array']),
    );
  }
}

class DataArray {
  final Complaint complaint;
  final List<ComplaintAction> complaintActions;

  DataArray({
    required this.complaint,
    required this.complaintActions,
  });

  factory DataArray.fromJson(Map<String, dynamic> json) {
    return DataArray(
      complaint: Complaint.fromJson(json['complaint']),
      complaintActions: List<ComplaintAction>.from(
        json['complaint_actions'].map(
          (action) => ComplaintAction.fromJson(action),
        ),
      ),
    );
  }
}

class Complaint {
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

  Complaint({
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

  factory Complaint.fromJson(Map<String, dynamic> json) {
    return Complaint(
      uid: json['uid'],
      createdOn: json['created_on'],
      updatedOn: json['updated_on'],
      createdBy: json['created_by'],
      // latitude: json['latitude'],
      // longitude: json['longitude'],
       latitude: json['latitude'] ?? '0.0',
      longitude: json['longitude'] ?? '0.0',
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
}

class ComplaintAction {
  final String id;
  final String uid;
  final String status;
  final String color;
  final double progress;
  final String createdOn;
  final String updatedOn;
  final String ip;
  final String serialNumber;
  final String startTime;
  final String endTime;
  final String duration;
  final String description;
  final String latitude;
  final String longitude;
  final String createdBy;
  final String updatedBy;
  final String complaint;
  final dynamic smsFrom;

  ComplaintAction({
    required this.id,
    required this.uid,
    required this.status,
    required this.color,
    required this.progress,
    required this.createdOn,
    required this.updatedOn,
    required this.ip,
    required this.serialNumber,
    required this.startTime,
    required this.endTime,
    required this.duration,
    required this.description,
    required this.latitude,
    required this.longitude,
    required this.createdBy,
    required this.updatedBy,
    required this.complaint,
    required this.smsFrom,
  });

  factory ComplaintAction.fromJson(Map<String, dynamic> json) {
    return ComplaintAction(
      id: json['id'] ?? "",
      uid: json['uid'] ?? "",
      status: json['status'] ?? "",
      color: json['color'] ?? "",
      progress: json['progress'].toDouble() ?? 0.0,
      createdOn: json['created_on'] ?? "",
      updatedOn: json['updated_on'] ?? "",
      ip: json['ip'] ?? "",
      serialNumber: json['serial_number'] ?? "",
      startTime: json['start_time'] ?? "",
      endTime: json['end_time'] ?? "",
      duration: json['duration'] ?? "",
      description: json['description'] ?? "",
      latitude: json['latitude'] ?? "",
      longitude: json['longitude'] ?? "",
      createdBy: json['created_by'] ?? "",
      updatedBy: json['updated_by'] ?? "",
      complaint: json['complaint'] ?? "",
      smsFrom: json['sms_from'] ?? "",
    );
  }
}

Map<String, dynamic> complaintModelToJson(ComplaintDetailModel model) {
  return {
    'status': model.status,
    'message': model.message,
    'data_array': dataArrayToJson(model.dataArray),
  };
}

Map<String, dynamic> dataArrayToJson(DataArray dataArray) {
  return {
    'complaint': complaintToJson(dataArray.complaint),
    'complaint_actions': dataArray.complaintActions
        .map((action) => complaintActionToJson(action))
        .toList(),
  };
}

Map<String, dynamic> complaintToJson(Complaint complaint) {
  return {
    'uid': complaint.uid,
    'created_on': complaint.createdOn,
    'updated_on': complaint.updatedOn,
    'created_by': complaint.createdBy,
    'latitude': complaint.latitude,
    'longitude': complaint.longitude,
    'ip': complaint.ip,
    'serial_number': complaint.serialNumber,
    'status': complaint.status,
    'area': complaint.area,
    'category': complaint.category,
    'subcategory': complaint.subcategory,
    'color': complaint.color,
    'description': complaint.description,
    'progress': complaint.progress,
  };
}

Map<String, dynamic> complaintActionToJson(ComplaintAction action) {
  return {
    'id': action.id,
    'uid': action.uid,
    'status': action.status,
    'color': action.color,
    'progress': action.progress,
    'created_on': action.createdOn,
    'updated_on': action.updatedOn,
    'ip': action.ip,
    'serial_number': action.serialNumber,
    'start_time': action.startTime,
    'end_time': action.endTime,
    'duration': action.duration,
    'description': action.description,
    'latitude': action.latitude,
    'longitude': action.longitude,
    'created_by': action.createdBy,
    'updated_by': action.updatedBy,
    'complaint': action.complaint,
    'sms_from': action.smsFrom,
  };
}
