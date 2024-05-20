;G28
;G90
;G0 F5000
;G0 X150 Y80 Z10
;G92 X0 Y0

; zvalues used with the "big oil tank"
; min z 130
; max z 150
; homing z 160

M83

G0 Z160
G28 XY
G0 F5000
G0 X150 Y80
G92 X0 Y0

G4 S2

;purge
G0 X-30
G0 Z135
;G1 F3600 E250
G1 F3600 E50
G0 Z140

G4 S2

; return to origin
G0 X0

; drawing a square
G0 X-10 Y-10 ; pos1
G0 Z135 ; plunging in the tank
G1 E10 ; pumping the water / ethanol mix (50 is a big droplet, 10 or a smaller one)
G0 Z140 ; retracting

G0 X10 Y-10
G0 Z135
G1 E10
G0 Z140

G0 X10 Y10
G0 Z135
G1 E10
G0 Z140

G0 X-10 Y10
G0 Z135
G1 E10
G0 Z140