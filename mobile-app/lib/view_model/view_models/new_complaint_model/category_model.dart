class ChatagoriData {
  final int status;
  final String message;
  final List<Item> responseData;

  ChatagoriData({
    required this.status,
    required this.message,
    required this.responseData,
  });

  factory ChatagoriData.fromJson(Map<String, dynamic> json) {
    List<dynamic> responseDataJson = json['response_data'];
    List<Item> responseData =
        responseDataJson.map((itemJson) => Item.fromJson(itemJson)).toList();

    return ChatagoriData(
      status: json['status'],
      message: json['message'],
      responseData: responseData,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'status': status,
      'message': message,
      'response_data': responseData,
    };
  }
}

class Item {
  final int id;
  final String name;
  final String parentSystemCode;
  final int userTypeId;
  final String userTypeName;
  final String code;
  final String systemCode;
  final String description;
  final int parent;
  final int lft;
  final int rght;
  final int treeId;
  final int mpttLevel;
  final String status;

  Item({
    required this.id,
    required this.name,
    required this.parentSystemCode,
    required this.userTypeId,
    required this.userTypeName,
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

  factory Item.fromJson(Map<String, dynamic> json) {
    return Item(
      id: json['id'] ?? 0,
      name: json['name'] ?? "",
      parentSystemCode: json['parent_system_code'],
      userTypeId: json['user_type_id'] ?? 0,
      userTypeName: json['user_type_name'] ?? "",
      code: json['code'],
      systemCode: json['system_code'],
      description: json['description'] ?? "",
      parent: json['parent'] ?? 0,
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
      'user_type_id': userTypeId,
      'user_type_name': userTypeName,
      'code': code,
      'system_code': systemCode,
      'description': description,
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
        'user_type_id: $userTypeId,\n'
        'user_type_name: $userTypeName,\n'
        'code: $code,\n'
        'system_code: $systemCode,\n'
        'description: $description,\n'
        'parent: $parent,\n'
        'lft: $lft,\n'
        'rght: $rght,\n'
        'tree_id: $treeId,\n'
        'mptt_level: $mpttLevel,\n'
        'status: $status,\n'
        '}';
  }
}
