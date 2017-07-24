[f,gof,output] = fit(Time,Voltage, a*(1-exp(-1200.0/b))*(1-exp(-x/b))+c+d*(1-exp(-1200.0/e))*(1-exp(-x/e))+f*(1-exp(-1200.0/g))*(1-exp(-x/g))','Startpoint',[0,20,0.0145,0.0119,300,0.1548,3000])
plot(f,Time,Voltage)
rsquare = num2str(gof.rsquare);
title(['fit SOC is 20%, I = 15 en R² = ' rsquare])
