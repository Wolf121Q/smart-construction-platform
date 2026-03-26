import 'package:http/http.dart' as http;

int requestCounter = 0;

Future<http.Response> logAndSendRequest(Future<http.Response> Function() requestFunction) async {
  requestCounter++;
  print('Request count: $requestCounter');
  final response = await requestFunction();

  print('Request to: ${response.request?.url}');
  print('Request method: ${response.request?.method}');
  print('Response status code: ${response.statusCode}');
  // Optionally log the response body if needed
  // print('Response body: ${response.body}');

  return response;
}
