@echo off
if defined FIMPP_JAVA_HOME (
  "%FIMPP_JAVA_HOME%\bin\java.exe" -jar "%~dp0Fimpp.jar" %*
) else if defined JAVA_HOME (
  "%JAVA_HOME%\bin\java.exe" -jar "%~dp0Fimpp.jar" %*
) else (
  java -jar "%~dp0Fimpp.jar" %*
)
