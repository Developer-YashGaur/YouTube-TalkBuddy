import 'dart:async';

import 'package:flutter/material.dart';
import 'package:talk_buddy/screens/welcome_screen.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    Timer(
        const Duration(seconds: 5),
        () => Navigator.pushReplacement(context,
            MaterialPageRoute(builder: (context) => const WelcomeScreen())));
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.white,
      // child: FlutterLogo(size: MediaQuery.of(context).size.height),
      child: const Center(
        child: Text(
          "TALKBUDDY",
          style: TextStyle(color: Colors.green, fontWeight: FontWeight.w900),
        ),
      ),
    );
  }
}
