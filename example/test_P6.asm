.text
case_1_begin:
	lui $0 , 39869
	lui $19, 5005
	lui $25, 50030
	lui $29, 53267
	lui $31, 27301
	ori $25, $0 , 60172
	jal case_1_1
	addi $25, $29, 5768
	multu $0 , $0 
	mfhi $0 
	jal case_1_2
	mthi $25
	ori $25, $0 , 0
	nop 
	nop 
	lh $29, 42($25)
case_1_1:
	ori $25, $0 , 0
	nop 
	nop 
	sw $0 , 80($25)
	ori $19, $0 , 0
	lh $19, 44($19)
	jr $31
	divu $29, $0 
	mflo $0 
case_1_2:
	or $0 , $25, $25
	ori $0 , $0 , 0
	nop 
	lh $25, 30($0)
	mthi $0 
	jal case_1_3
	andi $29, $19, 24879
	ori $25, $0 , 0
	nop 
	sh $31, 26($25)
	jal case_1_4
	andi $19, $0 , 37447
	ori $25, $0 , 0
	nop 
	nop 
	sw $31, 96($25)
case_1_3:
	ori $29, $0 , 0
	nop 
	nop 
	lw $25, 20($29)
	sltu $0 , $19, $25
	jr $31
	divu $31, $25
	mfhi $25
case_1_4:
	addi $25, $0 , -3707
	and $29, $0 , $31
	jal case_1_5
	mthi $25
	andi $29, $29, 56825
	jal case_1_6
	addi $31, $29, -2448
	andi $0 , $31, 6331
case_1_5:
	ori $29, $0 , 0
	nop 
	nop 
	sw $0 , 0($29)
	ori $29, $0 , 0
	nop 
	sw $0 , 24($29)
	jr $31
	ori $29, $0 , 0
	nop 
	nop 
	sh $0 , 30($29)
case_1_6:
	jal case_1_7
	addi $29, $25, -15989
	sltu $0 , $19, $31
	jal case_1_8
	slt $31, $25, $29
	addi $25, $25, -5527
case_1_7:
	addi $19, $19, 23349
	ori $19, $25, 15745
	jr $31
	andi $29, $29, 23287
case_1_8:
	lui $1 , 0
case_1_end:
case_2_begin:
	lui $0 , 1011
	lui $3 , 37325
	lui $12, 43117
	lui $23, 36465
	lui $31, 57664
	beq $3 , $0 , case_2_1
	addi $3 , $23, 24084
	ori $0 , $0 , 0
	sw $12, 28($0)
case_2_1:
	ori $0 , $0 , 0
	lw $3 , 28($0)
	div $12, $12
	mflo $23
	mthi $3 
	jal case_2_3
	and $23, $12, $0 
	ori $31, $0 , 0
	sb $31, 99($31)
	jal case_2_4
	mthi $12
	mtlo $3 
case_2_3:
	mtlo $12
	andi $0 , $0 , 61661
	jr $31
	ori $31, $0 , 0
	nop 
	lb $12, 75($31)
case_2_4:
	divu $31, $12
	mfhi $0 
	and $0 , $0 , $31
	jal case_2_7
	and $0 , $12, $0 
	ori $0 , $0 , 0
	nop 
	sh $0 , 18($0)
	jal case_2_8
	andi $31, $23, 51204
	multu $31, $3 
	mfhi $12
case_2_7:
	addi $3 , $23, -5382
	addi $0 , $23, -25798
	jr $31
	ori $23, $12, 41483
case_2_8:
	jal case_2_9
	add $3 , $0 , $12
	slt $3 , $3 , $0 
	jal case_2_10
	sltu $23, $23, $12
	mtlo $23
case_2_9:
	and $0 , $23, $23
	addi $12, $0 , 16642
	jr $31
	addi $12, $0 , -2758
case_2_10:
	addi $0 , $12, -23066
	lui $1 , 0
case_2_end:
case_3_begin:
	lui $0 , 56976
	lui $4 , 7955
	lui $17, 45590
	lui $29, 14360
	lui $31, 46505
	addi $17, $17, 538
	beq $4 , $31, case_3_1
	addi $31, $29, -30876
	div $4 , $4 
	mfhi $4 
case_3_1:
	and $29, $4 , $0 
	beq $17, $29, case_3_2
	ori $31, $17, 39981
	ori $4 , $0 , 0
	nop 
	nop 
	lw $0 , 72($4)
case_3_2:
	jal case_3_3
	mtlo $0 
	ori $17, $0 , 0
	nop 
	nop 
	lb $29, 20($17)
	jal case_3_4
	mtlo $0 
	sltu $0 , $31, $17
case_3_3:
	ori $0 , $0 , 0
	lh $4 , 16($0)
	ori $4 , $0 , 0
	nop 
	nop 
	sw $29, 0($4)
	jr $31
	addi $29, $31, 12384
case_3_4:
	andi $4 , $4 , 62018
	multu $17, $31
	mfhi $29
	andi $0 , $0 , 55192
	ori $29, $0 , 0
	nop 
	nop 
	lh $4 , 86($29)
	jal case_3_5
	andi $0 , $29, 56479
	ori $31, $0 , 0
	nop 
	lh $17, 96($31)
	jal case_3_6
	sub $4 , $17, $4 
	ori $4 , $0 , 0
	nop 
	lb $29, 25($4)
case_3_5:
	mtlo $0 
	ori $29, $29, 61634
	jr $31
	addi $17, $0 , 28827
case_3_6:
	lui $1 , 0
case_3_end:
case_4_begin:
	lui $0 , 50221
	lui $2 , 58304
	lui $6 , 16677
	lui $27, 54843
	lui $31, 49444
	ori $31, $0 , 0
	nop 
	nop 
	lw $27, 24($31)
	bne $31, $27, case_4_1
	sub $6 , $31, $27
	ori $6 , $0 , 0
	nop 
	lh $27, 82($6)
case_4_1:
	ori $0 , $2 , 5692
	jal case_4_2
	ori $2 , $27, 40389
	ori $6 , $0 , 0
	nop 
	nop 
	lb $0 , 28($6)
	jal case_4_3
	addi $2 , $0 , -22371
	divu $31, $31
	mfhi $27
case_4_2:
	addi $2 , $2 , 31181
	mtlo $6 
	jr $31
	ori $31, $0 , 0
	nop 
	nop 
	sb $0 , 70($31)
case_4_3:
	addi $0 , $31, -6238
	sub $2 , $6 , $0 
	sltu $2 , $2 , $6 
	jal case_4_4
	addi $2 , $27, -20707
	andi $6 , $0 , 16146
	jal case_4_5
	mthi $6 
	multu $6 , $27
	mflo $0 
case_4_4:
	ori $6 , $0 , 59079
	ori $6 , $0 , 0
	sb $0 , 2($6)
	jr $31
	ori $6 , $27, 48781
case_4_5:
	ori $0 , $0 , 0
	nop 
	nop 
	lw $6 , 76($0)
	ori $0 , $0 , 0
	lw $31, 28($0)
	lui $1 , 0
case_4_end:
case_5_begin:
	lui $0 , 2437
	lui $4 , 12317
	lui $8 , 1101
	lui $17, 3865
	lui $31, 63795
	jal case_5_1
	addi $4 , $17, 4876
	or $0 , $17, $17
	jal case_5_2
	and $0 , $17, $8 
	addi $31, $8 , -26688
case_5_1:
	multu $8 , $4 
	mfhi $0 
	addi $0 , $17, -6159
	jr $31
	divu $31, $4 
	mflo $17
case_5_2:
	beq $8 , $31, case_5_3
	addi $4 , $17, 16283
	ori $31, $0 , 0
	sb $4 , 3($31)
case_5_3:
	jal case_5_4
	or $8 , $17, $0 
	and $17, $31, $0 
	jal case_5_5
	andi $31, $17, 25037
	addi $17, $17, 26198
case_5_4:
	ori $4 , $0 , 5661
	ori $0 , $0 , 0
	nop 
	lw $17, 64($0)
	jr $31
	addi $31, $0 , -17960
case_5_5:
	div $4 , $17
	mflo $0 
	add $8 , $4 , $4 
	beq $4 , $8 , case_5_6
	addi $31, $4 , -27701
	addi $0 , $17, -3711
case_5_6:
	mult $17, $17
	mflo $17
	beq $0 , $4 , case_5_8
	sltu $31, $0 , $31
	mult $8 , $31
	mfhi $17
case_5_8:
	jal case_5_9
	add $4 , $17, $8 
	addi $8 , $4 , -21578
	jal case_5_10
	add $31, $8 , $8 
	ori $0 , $0 , 0
	nop 
	lw $0 , 76($0)
case_5_9:
	divu $17, $17
	mflo $0 
	mtlo $17
	jr $31
	and $31, $4 , $31
case_5_10:
	multu $8 , $4 
	mfhi $17
	lui $1 , 0
case_5_end:
case_6_begin:
	lui $0 , 3145
	lui $1 , 15310
	lui $14, 10479
	lui $15, 52296
	lui $31, 34
	beq $15, $15, case_6_1
	or $0 , $1 , $1 
	ori $0 , $0 , 0
	lw $1 , 56($0)
case_6_1:
	ori $1 , $0 , 0
	lb $1 , 18($1)
	ori $31, $0 , 0
	nop 
	nop 
	sw $15, 20($31)
	bne $31, $0 , case_6_2
	or $0 , $31, $1 
	ori $0 , $0 , 0
	lh $0 , 60($0)
case_6_2:
	addi $15, $15, -1748
	ori $15, $0 , 0
	lh $31, 22($15)
	andi $14, $31, 4249
	ori $1 , $0 , 0
	nop 
	lw $1 , 20($1)
	bne $1 , $1 , case_6_3
	andi $15, $15, 39514
	ori $1 , $0 , 0
	lb $15, 13($1)
case_6_3:
	mthi $31
	lui $1 , 0
case_6_end:
case_7_begin:
	lui $0 , 18646
	lui $7 , 33895
	lui $11, 41348
	lui $19, 37419
	lui $31, 2076
	andi $31, $7 , 10724
	ori $31, $0 , 0
	nop 
	nop 
	sh $0 , 22($31)
	bne $19, $11, case_7_1
	addi $31, $19, -22763
	andi $11, $0 , 48367
case_7_1:
	ori $0 , $0 , 0
	lw $19, 92($0)
	and $0 , $31, $19
	ori $0 , $0 , 0
	nop 
	sw $11, 32($0)
	ori $19, $0 , 0
	nop 
	nop 
	lb $7 , 53($19)
	ori $19, $0 , 0
	nop 
	sb $11, 68($19)
	add $31, $31, $11
	and $31, $0 , $0 
	lui $1 , 0
case_7_end:
case_8_begin:
	lui $0 , 58259
	lui $22, 26371
	lui $23, 5871
	lui $25, 5261
	lui $31, 17443
	ori $25, $0 , 0
	sh $0 , 60($25)
	mult $23, $22
	mflo $0 
	jal case_8_3
	or $0 , $23, $23
	addi $0 , $22, -11785
	jal case_8_4
	mthi $25
	mtlo $23
case_8_3:
	multu $0 , $25
	mfhi $0 
	ori $22, $23, 65512
	jr $31
	ori $22, $0 , 0
	lb $0 , 33($22)
case_8_4:
	addi $25, $31, -5771
	sub $22, $23, $23
	jal case_8_5
	mthi $25
	addi $25, $31, 24146
	jal case_8_6
	mtlo $31
	andi $0 , $23, 605
case_8_5:
	addi $23, $23, -274
	mthi $25
	jr $31
	mtlo $23
case_8_6:
	addi $0 , $23, -82
	ori $23, $0 , 0
	nop 
	nop 
	lb $25, 49($23)
	addi $0 , $25, -674
	mult $23, $31
	mfhi $0 
	lui $1 , 0
case_8_end:
case_9_begin:
	lui $0 , 4519
	lui $8 , 50966
	lui $12, 19517
	lui $20, 62898
	lui $31, 25146
	addi $12, $31, -7086
	addi $8 , $31, -8988
	beq $31, $12, case_9_1
	add $8 , $31, $20
	mtlo $0 
case_9_1:
	beq $8 , $12, case_9_2
	addi $0 , $31, -45
	ori $8 , $0 , 0
	sb $0 , 12($8)
case_9_2:
	sltu $31, $12, $8 
	ori $31, $0 , 0
	lb $31, 24($31)
	ori $8 , $0 , 0
	nop 
	sb $20, 66($8)
	mthi $12
	slt $12, $12, $31
	mthi $31
	lui $1 , 0
case_9_end:
case_10_begin:
	lui $0 , 30913
	lui $3 , 39410
	lui $6 , 35588
	lui $24, 39214
	lui $31, 36092
	mthi $0 
	mthi $31
	jal case_10_1
	mthi $6 
	addi $31, $24, 19534
	jal case_10_2
	mtlo $6 
	divu $0 , $0 
	mfhi $3 
case_10_1:
	addi $6 , $0 , 17286
	mtlo $6 
	jr $31
	mtlo $31
case_10_2:
	slt $6 , $24, $3 
	ori $0 , $3 , 1833
	mtlo $0 
	beq $31, $0 , case_10_3
	sltu $31, $31, $3 
	addi $31, $31, 5212
case_10_3:
	ori $6 , $0 , 0
	nop 
	lh $6 , 92($6)
	addi $3 , $6 , -4124
	jal case_10_4
	sltu $24, $0 , $24
	ori $3 , $0 , 0
	nop 
	nop 
	sh $24, 48($3)
	jal case_10_5
	and $3 , $31, $3 
	ori $24, $0 , 0
	nop 
	nop 
	lw $0 , 52($24)
case_10_4:
	and $6 , $3 , $3 
	sltu $3 , $24, $0 
	jr $31
	andi $3 , $24, 51773
case_10_5:
	lui $1 , 0
case_10_end:
