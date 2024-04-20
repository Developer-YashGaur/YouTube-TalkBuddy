import 'package:flutter/material.dart';
import 'package:talk_buddy/api_services/authentication.dart';
import 'package:talk_buddy/screens/login_screen.dart';
import 'package:talk_buddy/widgets/custom_scaffold.dart';

class UserDashboard extends StatelessWidget {
  final Map token;
  const UserDashboard({super.key, required this.token});

  @override
  Widget build(BuildContext context) {
    return CustomScaffold(
        child: Column(
      children: [
        Flexible(
          flex: 8,
          child: Container(
            padding: const EdgeInsets.symmetric(vertical: 0, horizontal: 40.0),
            child: Center(
              child: RichText(
                textAlign: TextAlign.center,
                text: const TextSpan(
                  children: [
                    TextSpan(
                      text: "Welcome Back \n",
                      style: TextStyle(
                          fontSize: 45.0, fontWeight: FontWeight.w600),
                    ),
                    TextSpan(
                      text: "\n Enter personal details to login in TalkBuddy",
                      style: TextStyle(
                        fontSize: 20,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
        Flexible(
          flex: 1,
          child: Align(
            alignment: Alignment.bottomRight,
            child: Row(
          children: [
            ElevatedButton(onPressed: () async {
              await logoutUser(refresh: token['refresh'], access: token['access']);
              // ignore: use_build_context_synchronously
              Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => const LoginScreen()));
            }, child: const Text('Log out'))
          ],
        )))
      ],
    ));
  }
}