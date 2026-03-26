

 class ComplaintStatus {
  int status;
  String message;
  List<StatusData> responseData;

  ComplaintStatus({required this.status, required this.message, required this.responseData});

  factory ComplaintStatus.fromJson(Map<String, dynamic> json) {
    return ComplaintStatus(
      status: json['status'],
      message: json['message'],
      responseData: (json['response_data'] as List)
          .map((data) => StatusData.fromJson(data))
          .toList(),
    );
  }
}

class StatusData {
  int id;
  String name;
  String parentSystemCode;
  String code;
  String systemCode;
  String color;
  int parent;
  int lft;
  int rght;
  int treeId;
  int mpttLevel;
  int status;

  StatusData({
    required this.id,
    required this.name,
    required this.parentSystemCode,
    required this.code,
    required this.systemCode,
    required this.color,
    required this.parent,
    required this.lft,
    required this.rght,
    required this.treeId,
    required this.mpttLevel,
    required this.status,
  });

  factory StatusData.fromJson(Map<String, dynamic> json) {
    return StatusData(
      id: json['id'],
      name: json['name'],
      parentSystemCode: json['parent_system_code'],
      code: json['code'],
      systemCode: json['system_code'],
      color: json['color'],
      parent: json['parent'],
      lft: json['lft'],
      rght: json['rght'],
      treeId: json['tree_id'],
      mpttLevel: json['mptt_level'],
      status: json['status'],
    );
  }
}
