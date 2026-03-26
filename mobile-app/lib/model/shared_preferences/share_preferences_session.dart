
import 'package:shared_preferences/shared_preferences.dart';

// void saveSessionData(Map<String, dynamic> jsonData) async {
//   final SharedPreferences prefs = await SharedPreferences.getInstance();
//   prefs.setBool('isLoggedIn', true);
//   prefs.setInt('status', jsonData['status']);
//   prefs.setString('message', jsonData['message'] ?? 'N/A');
//   prefs.setString('access_token', jsonData['access_token'] ?? 'N/A');
//   prefs.setInt('user_area_type_id', jsonData['user_area_type_id']);
//   prefs.setString('username', jsonData['username'] ?? 'N/A');
//   prefs.setString('email', jsonData['email'] ?? 'N/A');
//   prefs.setStringList('permissions', jsonData['permissions'] ?? []);
//   prefs.setInt('login_time', jsonData['login_time'] ?? 0);
// }
void saveSessionData(Map<String, dynamic> jsonData) async {
  final SharedPreferences prefs = await SharedPreferences.getInstance();
  prefs.setBool('isLoggedIn', true);
  prefs.setInt('status', jsonData['status']);
  prefs.setString('message', jsonData['message'] ?? 'N/A');
  prefs.setString('access_token', jsonData['access_token'] ?? 'N/A');
  prefs.setString('token_expiry_time',
      jsonData['token_expiry_time'] ?? 'N/A'); // Add this line
  prefs.setInt('user_area_type_id', jsonData['user_area_type_id']);
  prefs.setString('username', jsonData['username'] ?? 'N/A');
  prefs.setString('email', jsonData['email'] ?? 'N/A');
  prefs.setStringList(
      'permissions', List<String>.from(jsonData['permissions'] ?? []));
  prefs.setInt('login_time', jsonData['login_time'] ?? 0);
}

void logout() async {
  final SharedPreferences prefs = await SharedPreferences.getInstance();
  clearSharedPreferences();
  prefs.setBool('isLoggedIn', false);
  // prefs.setBool('isDashboard', false);
}

void clearSharedPreferences() async {
  SharedPreferences prefs = await SharedPreferences.getInstance();
  await prefs.clear();
}
