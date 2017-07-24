
%---------------Relaxation----------------
Rel = 1;
Dis = 0;
num = num+1;

switch Puls
    case 30.0
    startp = 1+Dis*4+Rel*2;
    endp = 3+Dis*4+Rel*2;
    case 50.0
    startp = 9+Dis*4+Rel*2;
    endp = 11+Dis*4+Rel*2;
    case 100.0
    startp = 17+Dis*4+Rel*2;
    endp =19+Dis*4+Rel*2;
    case 150.0
    startp = 25+Dis*4+Rel*2;
    endp =27+Dis*4+Rel*2;
    case 200.0
    startp =33+Dis*4+Rel*2;
    endp=35+Dis*4+Rel*2;
    case 0.0
    startp =41+Rel*2;
    endp = 43+Rel*2;
end

Times = HPPCcel125(startp:endp,Col);
Timings = [];
Timings(1,1) = Times(1);
Timings(2,1) = Times(2);
Timings(3,1) = Times(3);
Timings(4,1) = Times(2)+0.5;
Timings(5,1) = Times(2)+150.0;

Row = [];

[r index] = min(abs(timeSeconds(:,1)-Timings(1)));
Row(1)=index;

[r index] = min(abs(timeSeconds(:,1)-Timings(2)));
Row(2)=index;

[r index] = min(abs(timeSeconds(:,1)-Timings(3)));
Row(3)=index;

[r index] = min(abs(timeSeconds(:,1)-Timings(4)));
Row(4)=index;

[r index] = min(abs(timeSeconds(:,1)-Timings(5)));
Row(5)=index;

StartVoltage = Voltage(Row(1));
SearchedVoltage = Voltage(Row(2):Row(3),1);
Voltage05 = Voltage(Row(4));
Voltage150 = Voltage(Row(5));

SearchedTime = timeSeconds(Row(2):Row(3),1);
SearchedTime = SearchedTime - SearchedTime(1);

temp2 = num2str(Voltage150);
cur = num2str(Puls);
temp = '*a*-1000*(1-exp(-10/b))*exp(-x/b)+';
equation = strcat(cur,temp,temp2);

[f,gof,output] = fit(SearchedTime,SearchedVoltage,equation,'Startpoint',[0.001,20]);

fig = figure;
plot(f,SearchedTime,SearchedVoltage);
rsquare = num2str(gof.rsquare);
xlabel('Voltage in mV');
ylabel('Time in Seconds');
titl = strcat('fit DOD = ',num2str(DODinit),' current is ',cur,'A en R² = ',rsquare);
figname = strcat('DOD',num2str(DODinit),'I',cur,'num',num2str(num),'.fig');
title(titl);
savefig(fig,figname);
close(fig);

param = [];
Coeff = coeffvalues(f);
param(1) = (Voltage05-StartVoltage)/(Puls*1000.0);     %R0 Value
param(2) = Coeff(1);                                   %R1 value
param(3) = Coeff(2)/param(2);                          %C1 Value
param(4) = Coeff(2);                                   %Timeconstant
param(5) = gof.rsquare;                                %R²



Totalparam(:,num)=param;
%------------------------------Go to Current----------
num=num+1;
Rel = 0;

switch Puls
    case 30.0
    startp = 1+Dis*4+Rel*2;
    endp = 3+Dis*4+Rel*2;
    case 50.0
    startp = 9+Dis*4+Rel*2;
    endp = 11+Dis*4+Rel*2;
    case 100.0
    startp = 17+Dis*4+Rel*2;
    endp =19+Dis*4+Rel*2;
    case 150.0
    startp = 25+Dis*4+Rel*2;
    endp =27+Dis*4+Rel*2;
    case 200.0
    startp =33+Dis*4+Rel*2;
    endp=35+Dis*4+Rel*2;
    case 0.0
    startp =41+Rel*2;
    endp = 43+Rel*2;
end

Times = HPPCcel125(startp:endp,Col);
Timings = [];
Timings(1,1) = Times(1);
Timings(2,1) = Times(2);
Timings(3,1) = Times(3);
Timings(4,1) = Times(2)+0.5;

Row = [];

[r index] = min(abs(timeSeconds(:,1)-Timings(1)));
Row(1)=index;

[r index] = min(abs(timeSeconds(:,1)-Timings(2)));
Row(2)=index;

[r index] = min(abs(timeSeconds(:,1)-Timings(3)));
Row(3)=index;

[r, index] = min(abs(timeSeconds(:,1)-Timings(4)));
Row(4)=index;

StartVoltage = Voltage(Row(1));
SearchedVoltage = [];
SearchedVoltage = Voltage(Row(2):Row(3),1);
Voltage05 = Voltage(Row(4));
Voltage150 = [];

SearchedTime = [];
SearchedTime = timeSeconds(Row(2):Row(3),1);
SearchedTime = SearchedTime - SearchedTime(1);

temp2 = num2str(Voltage05);
constante = param(4);
cons = num2str(constante);
cur = num2str(Puls);
temp = '*a*-1000*(1-exp(-x/';
temp3='))+';
equation = strcat(cur,temp,cons,temp3,temp2);

[f,gof,output] = fit(SearchedTime,SearchedVoltage,equation,'Startpoint',[0.001]);

fig = figure;
plot(f,SearchedTime,SearchedVoltage);
rsquare = num2str(gof.rsquare);
xlabel('Voltage in mV');
ylabel('Time in Seconds');
titl = strcat('fit DOD = ',num2str(DODinit),' current is ',cur,'A en R² = ',rsquare);
figname = strcat('DOD',num2str(DODinit),'I',cur,'num',num2str(num),'.fig');
title(titl);
savefig(fig,figname);
close(fig);

param = [];
Coeff = coeffvalues(f);
param(1) = (Voltage05-StartVoltage)/(Puls*1000.0);     %R0 Value
param(2) = Coeff(1);                                   %R1 value
param(3) = constante/param(2);                          %C1 Value
param(4) = constante;                                 %Timeconstant
param(5) = gof.rsquare;                                %R²



Totalparam(:,num)=param;
%------------------------------Go to charging relax----------

Rel = 1;
Dis = 1;
num = num+1;

switch Puls
    case 30.0
    startp = 1+Dis*4+Rel*2;
    endp = 3+Dis*4+Rel*2;
    case 50.0
    startp = 9+Dis*4+Rel*2;
    endp = 11+Dis*4+Rel*2;
    case 100.0
    startp = 17+Dis*4+Rel*2;
    endp =19+Dis*4+Rel*2;
    case 150.0
    startp = 25+Dis*4+Rel*2;
    endp =27+Dis*4+Rel*2;
    case 200.0
    startp =33+Dis*4+Rel*2;
    endp=35+Dis*4+Rel*2;
    case 0.0
    startp =41+Rel*2;
    endp = 43+Rel*2;
end

Times = HPPCcel125(startp:endp,Col);
Timings = [];
Timings(1,1) = Times(1);
Timings(2,1) = Times(2);
Timings(3,1) = Times(3);
Timings(4,1) = Times(2)+0.5;
Timings(5,1) = Times(2)+150.0;

Row = [];

[r index] = min(abs(timeSeconds(:,1)-Timings(1)));
Row(1)=index;

[r index] = min(abs(timeSeconds(:,1)-Timings(2)));
Row(2)=index;

[r index] = min(abs(timeSeconds(:,1)-Timings(3)));
Row(3)=index;

[r index] = min(abs(timeSeconds(:,1)-Timings(4)));
Row(4)=index;

[r index] = min(abs(timeSeconds(:,1)-Timings(5)));
Row(5)=index;

StartVoltage = Voltage(Row(1));
SearchedVoltage = Voltage(Row(2):Row(3),1);
Voltage05 = Voltage(Row(4));
Voltage150 = Voltage(Row(5));

SearchedTime = timeSeconds(Row(2):Row(3),1);
SearchedTime = SearchedTime - SearchedTime(1);

temp2 = num2str(Voltage150);
cur = num2str(Puls);
temp = '*a*1000*(1-exp(-10/b))*exp(-x/b)+';
equation = strcat(cur,temp,temp2);

[f,gof,output] = fit(SearchedTime,SearchedVoltage,equation,'Startpoint',[0.001,20]);

fig = figure;
plot(f,SearchedTime,SearchedVoltage);
rsquare = num2str(gof.rsquare);
xlabel('Voltage in mV');
ylabel('Time in Seconds');
titl = strcat('fit DOD = ',num2str(DODinit),' current is ',cur,'A en R² = ',rsquare);
figname = strcat('DOD',num2str(DODinit),'I',cur,'num',num2str(num),'.fig');
title(titl);
savefig(fig,figname);
close(fig);

param = [];
Coeff = coeffvalues(f);
param(1) = (StartVoltage-Voltage05)/(Puls*1000.0);     %R0 Value
param(2) = Coeff(1);                                   %R1 value
param(3) = Coeff(2)/param(2);                          %C1 Value
param(4) = Coeff(2);                                   %Timeconstant
param(5) = gof.rsquare;                                %R²



Totalparam(:,num)=param;

%------------------------------Go to charging with current----------
num=num+1;
Rel = 0;

switch Puls
    case 30.0
    startp = 1+Dis*4+Rel*2;
    endp = 3+Dis*4+Rel*2;
    case 50.0
    startp = 9+Dis*4+Rel*2;
    endp = 11+Dis*4+Rel*2;
    case 100.0
    startp = 17+Dis*4+Rel*2;
    endp =19+Dis*4+Rel*2;
    case 150.0
    startp = 25+Dis*4+Rel*2;
    endp =27+Dis*4+Rel*2;
    case 200.0
    startp =33+Dis*4+Rel*2;
    endp=35+Dis*4+Rel*2;
    case 0.0
    startp =41+Rel*2;
    endp = 43+Rel*2;
end

Times = HPPCcel125(startp:endp,Col);
Timings = [];
Timings(1,1) = Times(1);
Timings(2,1) = Times(2);
Timings(3,1) = Times(3);
Timings(4,1) = Times(2)+0.5;

Row = [];

[r index] = min(abs(timeSeconds(:,1)-Timings(1)));
Row(1)=index;

[r index] = min(abs(timeSeconds(:,1)-Timings(2)));
Row(2)=index;

[r index] = min(abs(timeSeconds(:,1)-Timings(3)));
Row(3)=index;

[r, index] = min(abs(timeSeconds(:,1)-Timings(4)));
Row(4)=index;

StartVoltage = Voltage(Row(1));
SearchedVoltage = [];
SearchedVoltage = Voltage(Row(2):Row(3),1);
Voltage05 = Voltage(Row(4));
Voltage150 = [];

SearchedTime = [];
SearchedTime = timeSeconds(Row(2):Row(3),1);
SearchedTime = SearchedTime - SearchedTime(1);

temp2 = num2str(Voltage05);
constante = param(4);
cons = num2str(constante);
cur = num2str(Puls);
temp = '*a*1000*(1-exp(-x/';
temp3='))+';
equation = strcat(cur,temp,cons,temp3,temp2);

[f,gof,output] = fit(SearchedTime,SearchedVoltage,equation,'Startpoint',[0.001]);

fig = figure;
plot(f,SearchedTime,SearchedVoltage);
rsquare = num2str(gof.rsquare);
xlabel('Voltage in mV');
ylabel('Time in Seconds');
titl = strcat('fit DOD = ',num2str(DODinit),' current is ',cur,'A en R² = ',rsquare);
figname = strcat('DOD',num2str(DODinit),'I',cur,'num',num2str(num),'.fig');
title(titl);
savefig(fig,figname);
close(fig);

param = [];
Coeff = coeffvalues(f);
param(1) = (Voltage05-StartVoltage)/(Puls*1000.0);     %R0 Value
param(2) = Coeff(1);                                   %R1 value
param(3) = constante/param(2);                          %C1 Value
param(4) = constante;                                 %Timeconstant
param(5) = gof.rsquare;                                %R²



Totalparam(:,num)=param;

