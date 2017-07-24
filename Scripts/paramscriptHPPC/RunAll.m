DODinit = 120;

PulsRow = [30.0,50.0,100.0,150.0,200.0];
num = 0;

Totalparam = [];


while DODinit <121
    
    Col = (DODinit/6)+1;
    val = 1;
    while val < 6
        Puls = PulsRow(val);
        
        run('TOTAL.m');
        
        
        val=val+1;
    end
    DODinit = DODinit + 6;
end

filename = 'parameters.xlsx';
xlswrite(filename,Totalparam,'Blad1','A10');

