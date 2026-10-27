#!/usr/bin/env python3
"""
Mapper para Análisis de Consumo Eléctrico y Emisiones de CO2 (Hadoop MapReduce)
Entrada: Líneas CSV desde stdin con formato:
RecordID,Timestamp,MeterID,Zone,SectorType,ActivePower_kWh,Voltage_V,CarbonEmission_kgCO2,PeakHour
Salida: Clave-Valor delimitado por tabulador:
<Zone>  <ActivePower_kWh>,<CarbonEmission_kgCO2>,1
"""
import sys

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line or line.startswith("RecordID"):
            continue
        
        parts = line.split(",")
        if len(parts) >= 8:
            zone = parts[3].strip()
            try:
                active_power = float(parts[5].strip())
                carbon_emission = float(parts[7].strip())
                # Emitir Clave: Zona | Valor: Consumo,Emision,Contador
                print(f"{zone}\t{active_power:.3f},{carbon_emission:.4f},1")
            except ValueError:
                # Omitir registros corruptos o con formato inválido
                continue

if __name__ == "__main__":
    main()
