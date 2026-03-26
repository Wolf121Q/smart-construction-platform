class ComplaintStatusesModel {
  final int id;
  final String name;
  final String parentSystemCode;
  final String code;
  final String systemCode;
  final String color;
  final int parent;
  final int lft;
  final int rght;
  final int treeId;
  final int mpttLevel;
  final int status;

  ComplaintStatusesModel({
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

  factory ComplaintStatusesModel.fromJson(Map<String, dynamic> json) {
    return ComplaintStatusesModel(
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

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'parent_system_code': parentSystemCode,
      'code': code,
      'system_code': systemCode,
      'color': color,
      'parent': parent,
      'lft': lft,
      'rght': rght,
      'tree_id': treeId,
      'mptt_level': mpttLevel,
      'status': status,
    };
  }

  @override
  String toString() {
    return '{\n'
        'id: $id,\n'
        'name: $name,\n'
        'parent_system_code: $parentSystemCode,\n'
        'code: $code,\n'
        'system_code: $systemCode,\n'
        'color: $color,\n'
        'parent: $parent,\n'
        'lft: $lft,\n'
        'rght: $rght,\n'
        'tree_id: $treeId,\n'
        'mptt_level: $mpttLevel,\n'
        'status: $status,\n'
        '}';
  }
}
