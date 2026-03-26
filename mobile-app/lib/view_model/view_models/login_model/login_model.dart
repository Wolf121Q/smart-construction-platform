class LogInModel {
  final int status;
  final String message;
  final String accessToken;
  final String tokenExpiryTime;
  final int userAreaTypeId;
  final String username;
  final String email;
  final List<String> permissions;

  LogInModel({
    required this.status,
    required this.message,
    required this.accessToken,
    required this.tokenExpiryTime,
    required this.userAreaTypeId,
    required this.username,
    required this.email,
    required this.permissions,
  });

  factory LogInModel.fromJson(Map<String, dynamic> json) {
    List<dynamic> permissionsList = json['permissions'] ?? [];

    List<String> permissions =
        permissionsList.map((permission) => permission.toString()).toList();

    return LogInModel(
      status: json['status'] ?? 0,
      message: json['message'] ?? "",
      accessToken: json['access_token'] ?? "",
      tokenExpiryTime: json['token_expiry_time'] ?? "",
      userAreaTypeId: json['user_area_type_id'] ?? 0,
      username: json['username'] ?? "",
      email: json['email'] ?? "",
      permissions: permissions,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'status': status,
      'message': message,
      'access_token': accessToken,
      'token_expiry_time': tokenExpiryTime,
      'user_area_type_id': userAreaTypeId,
      'username': username,
      'email': email,
      'permissions': permissions, // Keep as a list
    };
  }
}


// class LogInModel {
//   final int status;
//   final String message;
//   final String accessToken;
//   final int userAreaTypeId;
//   final String username;
//   final String email;
//   final List<String> permissions;

//   LogInModel({
//     required this.status,
//     required this.message,
//     required this.accessToken,
//     required this.userAreaTypeId,
//     required this.username,
//     required this.email,
//     required this.permissions,
//   });

//   factory LogInModel.fromJson(Map<String, dynamic> json) {
//     List<dynamic> permissionsList = [];

//     if (json['permissions'] != null) {
//       permissionsList = json['permissions'];
//     } else {
//       permissionsList = [];
//     }

//     List<String> permissions =
//         permissionsList.map((permission) => permission.toString()).toList();

//     return LogInModel(
//       status: json['status'] ?? 0,
//       message: json['message'] ?? "",
//       accessToken: json['access_token'] ?? "",
//       userAreaTypeId: json['user_area_type_id'] ?? 0,
//       username: json['username'] ?? "",
//       email: json['email'] ?? "",
//       permissions: permissions,
//     );
//   }

//   Map<String, dynamic> toJson() {
//     return {
//       'status': status,
//       'message': message,
//       'accessToken': accessToken,
//       'userAreaTypeId': userAreaTypeId,
//       'username': username,
//       'email': email,
//       'permissions':
//           permissions.join(','), // Convert list to comma-separated string
//     };
//   }
// }
