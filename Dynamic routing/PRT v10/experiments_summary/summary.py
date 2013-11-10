summary_txt = open('experiments summary.txt', 'w')
for i in [1000, 2000, 3000]:
    for j in range(54):
        num = i + j
        with open('ex%d.txt' % num, 'r') as fp:
            NN_funcion, args = fp.readline().split('_')
            v_NN = NN_funcion[len('<function NN'):-len(' at 0x00000000025EF2E8>')]
            meanTimeArrival, imbalanceLevel, numOfPRTs = args.split(' ')
            v_meanTimeArrival, v_imbalanceLevel, v_numOfPRTs = meanTimeArrival[len('meanTimeArrival('):-len(')')], imbalanceLevel[len('imbalanceLevel('):-len(')')], numOfPRTs[len('numOfPRTs('):-len(') ')] 
            print fp.readline()
            v_compuTime = fp.readline()[len('computation time: '):-1]
            print fp.readline()
            print fp.readline()
            TTDistance = fp.readline()[len('T.TravedDist: '):-1]
            TETDistance = fp.readline()[len('T.E.TravelDist: '):-1]
            TFTime = fp.readline()[len('T.FlowTime: '):-1]
            TWTime = fp.readline()[len('T.WaitTime: '):-1]
            AWTime = fp.readline()[len('A.WaitTime: '):-1]
            IdleState = fp.readline()[len('IdleState_time: '):-1]
            ISTime, ISP = IdleState[:IdleState.index('(')], IdleState[IdleState.index('(') + 1:IdleState.index(')')]
            ApporachingState = fp.readline()[len('ApproachingState_time: '):-1]
            ASTime, ASP = ApporachingState[:ApporachingState.index('(')], ApporachingState[ApporachingState.index('(') + 1:ApporachingState.index(')')]
            SdleState = fp.readline()[len('SettingState_time: '):-1]
            SSTime, SSP = SdleState[:SdleState.index('(')], SdleState[SdleState.index('(') + 1:SdleState.index(')')]
            TdleState = fp.readline()[len('TransitingState_time: '):-1]
            TSTime, TSP = TdleState[:TdleState.index('(')], TdleState[TdleState.index('(') + 1:TdleState.index(')')]
            summary_txt.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n' % (v_NN, v_meanTimeArrival, v_imbalanceLevel, v_numOfPRTs, v_compuTime, TTDistance, TETDistance , TFTime, TWTime, AWTime, ISTime, ISP, ASTime, ASP, SSTime, SSP, TSTime, TSP)) 
