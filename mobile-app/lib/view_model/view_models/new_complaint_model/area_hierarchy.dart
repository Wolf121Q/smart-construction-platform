class AreaHierarchy {
  final int id;
  final String name;
  final String parentSystemCode;
  final String code;
  final String systemCode;
  final int? parent;
  final int lft;
  final int rght;
  final int treeId;
  final int mpttLevel;
  final int status;

  AreaHierarchy({
    required this.id,
    required this.name,
    required this.parentSystemCode,
    required this.code,
    required this.systemCode,
    this.parent,
    required this.lft,
    required this.rght,
    required this.treeId,
    required this.mpttLevel,
    required this.status,
  });

  factory AreaHierarchy.fromJson(Map<String, dynamic> json) {
    return AreaHierarchy(
      id: json['id'],
      name: json['name'],
      parentSystemCode: json['parent_system_code'],
      code: json['code'],
      systemCode: json['system_code'],
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
      'parent': parent,
      'lft': lft,
      'rght': rght,
      'tree_id': treeId,
      'mptt_level': mpttLevel,
      'status': status,
    };
  }
}
