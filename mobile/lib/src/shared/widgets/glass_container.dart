import 'dart:ui';
import 'package:flutter/material.dart';

class GlassContainer extends StatelessWidget {
  final Widget child;
  final double blur;
  final Color color;
  final BorderRadiusGeometry borderRadius;
  final EdgeInsetsGeometry? padding;
  final Border? border;

  const GlassContainer({
    super.key,
    required this.child,
    this.blur = 12.0,
    this.color = const Color(0xB3FFFFFF), // rgba(255, 255, 255, 0.7)
    this.borderRadius = const BorderRadius.all(Radius.circular(12)),
    this.padding,
    this.border,
  });

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: borderRadius,
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: blur, sigmaY: blur),
        child: Container(
          decoration: BoxDecoration(
            color: color,
            borderRadius: borderRadius,
            border: border,
          ),
          padding: padding,
          child: child,
        ),
      ),
    );
  }
}
