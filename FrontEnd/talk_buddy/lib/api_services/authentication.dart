import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:talk_buddy/main.dart';


Future<Map> loginUser({String? mobileNumber, String? password}) async {
    try{
      var response = await http.post(Uri.parse('$host/api/login'),
      body: jsonEncode({
        'mobileNumber': mobileNumber,
        'password': password
      },),
      headers: {
        'Content-Type': 'application/json'
      });

      // debugPrint(apiResponse.toString());
      if (response.statusCode == 200){
        return jsonDecode(response.body);
      }else{
        return {};
      }
    }
    catch(e) {
      rethrow;
    }
      // ignore: avoid_print
    // print(jsonDecode(response.body.toString()));
  }

Future<void> logoutUser({String? refresh, String? access}) async {
  try{
    var response = await http.post(Uri.parse('$host/api/logout'),
    body: jsonEncode({
      'refresh_token': refresh
    }),
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $access'
    },);

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }else{
    }
  }
  catch(e){
    rethrow;
  }
}