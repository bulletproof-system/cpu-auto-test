.data
	stack: .space 1000

.text
	beq $0, $0, if
	ori $2, $0, 123

if: