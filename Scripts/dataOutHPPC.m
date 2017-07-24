DODinit = input('Enter DOD(0,6,12,18,…,120): ');
Puls = input('Enter puls current: (or enter 0 for SOC change interval): ');
Dis = input('Enter 1 for charging and enter 0 for discharging: ');
Rel = input('Relaxing enter 1 or Current enter 0: ');
Col = (DODinit/6)+1;
switch Puls
    case 30
    startp = 1+Dis*4+Rel*2;
    endp = 3+Dis*4+Rel*2;
    case 50
    startp = 9+Dis*4+Rel*2;
    endp = 11+Dis*4+Rel*2;
    case 100
    startp = 17+Dis*4+Rel*2;
    endp =19+Dis*4+Rel*2;
    case 150
    startp = 25+Dis*4+Rel*2;
    endp =27+Dis*4+Rel*2;
    case 200
    startp =33+Dis*4+Rel*2;
    endp=35+Dis*4+Rel*2;
    case 0
    startp =41+Rel*2;
    endp = 43+Rel*2;
end

Times = HPPCcel125(startp:endp,Col);
n=1;
Row =[];

while n < 4
    Row(n) = find(timeSeconds(:,1) == Times(n));
    n=n+1;
end
VoltageStart = Voltage(Row(1));
SearchedVoltage = Voltage(Row(2):Row(3),1);

SearchedTime = []
n=0;
while n <(Row(3)-Row(2)+1)
    SearchedTime(n+1,1)=n;
    n=n+1;
end

plot(SearchedTime,SearchedVoltage)
