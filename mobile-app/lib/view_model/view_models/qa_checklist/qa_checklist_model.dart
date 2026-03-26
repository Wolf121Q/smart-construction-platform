class QAChecklistItem {
  int id;
  String name;
  String parentName;
  String parentSystemCode;
  String code;
  String systemCode;
  String description;
  int parent;
  int lft;
  int rght;
  int treeId;
  int mpttLevel;
  String status;

  QAChecklistItem({
    required this.id,
    required this.name,
    required this.parentName,
    required this.parentSystemCode,
    required this.code,
    required this.systemCode,
    required this.description,
    required this.parent,
    required this.lft,
    required this.rght,
    required this.treeId,
    required this.mpttLevel,
    required this.status,
  });

  factory QAChecklistItem.fromJson(Map<String, dynamic> json) {
    return QAChecklistItem(
      id: json['id'] ?? 0,
      name: json['name'] ?? "",
      parentName: json['parent_name'] ?? "",
      parentSystemCode: json['parent_system_code'] ?? "",
      code: json['code'] ?? "",
      systemCode: json['system_code'] ?? "",
      description: json['desription'] ?? "",
      parent: json['parent'] ?? 0,
      lft: json['lft'] ?? 0,
      rght: json['rght'] ?? 0,
      treeId: json['tree_id'] ?? 0,
      mpttLevel: json['mptt_level'] ?? 0,
      status: json['status'] ?? "",
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'parent_name': parentName,
      'parent_system_code': parentSystemCode,
      'code': code,
      'system_code': systemCode,
      'desription': description,
      'parent': parent,
      'lft': lft,
      'rght': rght,
      'tree_id': treeId,
      'mptt_level': mpttLevel,
      'status': status,
    };
  }
}
