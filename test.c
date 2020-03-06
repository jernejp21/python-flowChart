static void init714m(UB slot){ //fv:startStop init714m
/***	ローカル変数		***/
	ER	local_ledctl;							/*	LED点灯制御結果			*/
	UB	loop_portcnt;							/*	ループポートカウント	*/
	UH	local_slotpos;							/*	スロット実装位置		*/
	
/***	処理開始			***/
	if((slot < (UB)1u) || (slot > TM_SLOTMAX)){	/*	fc:ifBranch 引数異常?			*/
		l_softerrloop();						/*	fc:middleware ソフトエラーループ処理	*/
	}else{
												/*	fc:end 処理なし				*/
	}
	local_ledctl = mdl_ioled_ctl((UH)slot, (UH)NORMAL_LED, LAMP_G, EXFDO_UNIT);
												/*	fc:middleware fc:process IOユニットLED制御ミドルウェア	*/
	l_softerrchk(local_ledctl);					/*	fc:middleware ソフトウェアエラー判定処理	*/
	mdlexfctlwt.exfdoslot_umu |= (UW)((UW)0x0001u << (slot - 1u));
												/*	fc:process 汎用出力ユニット 割付有無編集	*/
	for(loop_portcnt = 0u; loop_portcnt < EXFDO_PORT_MAX; loop_portcnt++){
												/*	fc:forLoop ポート数分ループ		*/
		if(iosetupinfct.iosetinf[eqpinfwt.partno - 1u].slot[slot - 1u].bitinf[loop_portcnt] != 0u){
												/*	fc:ifBranch ビット割付有?			*/
			mdlexfctlwt.port_umu[slot - 1u] |= (UB)(0x01u << loop_portcnt);
												/*	fc:process 汎用出力ユニット ポート有無編集	*/
		}else{
												/*	fc:end 処理なし				*/
		}
	} //fc:end
	l_memcpy((UB *)&mdlexfctlwt.bit_umu[slot - 1u].port[0u], (UB *)&iosetupinfct.iosetinf[eqpinfwt.partno - 1u].slot[slot - 1u].bitinf[0u], EXFDO_PORT_MAX);
												/*	fc:middleware メモリコピー処理		*/
	if(mdlexfctlwt.snserrcnt == 0u){			/*	fc:ifBranch 異常確定数未設定?		*/
		mdlexfctlwt.snserrcnt = DO_SNSERRCNT_LIMIT;
												/*	fc:process 汎用出力ユニット センサKショート故障確定編集	*/
		mdlexfctlwt.cirerrcnt = ERRCNT_LIMIT;	/*	fc:process 汎用出力ユニット 制御回路故障確定数編集	*/
	}else{
												/*	fc:end 処理なし				*/
	}
	unitinfwt.exfdounit.insrtcnt += 1u;			/*	fc:process 汎用出力ユニット 実装枚数更新	*/
	local_slotpos = (unitinfwt.exfdounit.insrtcnt - 1u);
												/*	fc:process 汎用出力ユニット 実装枚数配列用設定	*/
	unitinfwt.exfdounit.insrtno[local_slotpos] = slot;
												/*	fc:process 汎用出力ユニット 実装位置設定する	*/
}//fv:startStop init714m