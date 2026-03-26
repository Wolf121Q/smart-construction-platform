
class DashboardChatModel {
  int? status;
  String? message;
  List<DataItem>? data;

  DashboardChatModel({
    this.status,
    this.message,
    this.data,
  });

  factory DashboardChatModel.fromJson(Map<String, dynamic> json) {
    List<dynamic> dataList = json['data'] ?? [];
    List<DataItem> dataItems =
        dataList.map((item) => DataItem.fromJson(item)).toList();

    return DashboardChatModel(
      status: json['status'],
      message: json['message'],
      data: dataItems,
      // responseData: (json['response_data'] as List)
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'status': status,
      'message': message,
      'data': data,
    };
  }
}

class DataItem {
  String name;
  String code;
  int total;
  String color;

  DataItem({
    required this.name,
    required this.code,
    required this.total,
    required this.color,
  });

  factory DataItem.fromJson(Map<String, dynamic> json) {
    return DataItem(
      name: json['name'],
      code: json['code'],
      total: json['total'],
      color: json['color'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'code': code,
      'total': total,
      'color': color,
    };
  }
}
