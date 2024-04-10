import 'package:flutter/material.dart';
import 'package:talk_buddy/screens/login_screen.dart';
import 'package:talk_buddy/screens/signup_screen.dart';
import 'package:talk_buddy/theme/theme.dart';
import 'package:talk_buddy/widgets/custom_scaffold.dart';
import 'package:talk_buddy/widgets/welcome_button.dart';

class WelcomeScreen extends StatelessWidget {
  const WelcomeScreen({super.key});

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
            const Expanded(
              child: WelcomeButton(
                buttonText: 'Sign In',
                onTap: LoginScreen(),
                color: Colors.transparent,
                textColor: Colors.white,
              ),
            ),
            Expanded(
              child: WelcomeButton(
                buttonText: 'Sign Up',
                onTap: const SignUpScreen(),
                color: Colors.white,
                textColor: lightColorScheme.primary,
              ),
            ),
          ],
        )))
      ],
    ));
  }
}
