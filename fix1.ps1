$iconPath = "C:\Users\consu\OneDrive\Documents\HCS_from_pi\jupyter-DSL\_output\static\favicons"
takeown /F $iconPath /R
icacls $iconPath /grant administrators:F /T
Remove-Item $iconPath -Force -Recurse
