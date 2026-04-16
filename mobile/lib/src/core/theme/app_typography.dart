import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'app_colors.dart';

class AppTypography {
  static final TextTheme textTheme = TextTheme(
    displayLarge: GoogleFonts.manrope(
      fontSize: 56, // 3.5rem
      fontWeight: FontWeight.w700,
      color: AppColors.onSurface,
    ),
    headlineMedium: GoogleFonts.manrope(
      fontSize: 28, // 1.75rem
      fontWeight: FontWeight.w600,
      color: AppColors.onSurface,
    ),
    titleLarge: GoogleFonts.inter(
      fontSize: 22, // 1.375rem
      fontWeight: FontWeight.w500,
      color: AppColors.onSurface,
    ),
    bodyMedium: GoogleFonts.inter(
      fontSize: 14, // 0.875rem
      fontWeight: FontWeight.w400,
      color: AppColors.onSurface,
    ),
    labelMedium: GoogleFonts.inter(
      fontSize: 12, // 0.75rem
      fontWeight: FontWeight.w600,
      color: AppColors.onSurface,
      letterSpacing: 1.2,
    ),
  );
}
