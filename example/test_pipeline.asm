.data
	stack: .space 1000

.text
	ori $2, $0, 3
	sw $2, 0($0)
	nop
	lw $2, 0($0)
	ori $3, $0, 3
	jal dfs
	sw $2, 0($0)
	lw $2, 0($0)
	lw $2, 0($0)
	add $3, $3, $2
	add $4, $2, $3
	jal end

dfs:sub $4, $2, $3
	jr $ra

end:
	sw $3, 0($0)
	sw $4, 0($0)