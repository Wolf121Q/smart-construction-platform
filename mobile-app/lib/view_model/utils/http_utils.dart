import 'package:dha_ctt_app/model/apis/request_logger.dart';
import 'package:http/http.dart' as http;

Future<http.Response> getRequest(Uri uri, {Map<String, String>? headers}) {
  return logAndSendRequest(() => http.get(uri, headers: headers));
}

// Similarly, you can add wrappers for other HTTP methods if needed
