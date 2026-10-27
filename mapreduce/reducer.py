#!/usr/bin/env python3
"""
Reducer para Análisis de Consumo Eléctrico y Emisiones de CO2 (Hadoop MapReduce)
Entrada: Clave-Valor ordenados por Hadoop Shuffle/Sort:
<Zone>  <ActivePower_kWh>,<CarbonEmission_kgCO2>,1
Salida: Estadísticas consolidadas por zona para toma de decisiones sostenibles
"""
import sys

def main():
    current_zone = None
    total_power = 0.0
    total_emissions = 0.0
    total_count = 0

    print("Zona\tLecturas\tConsumo_Total_kWh\tConsumo_Promedio_kWh\tEmisiones_CO2_kg")

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split("\t")
        if len(parts) != 2:
            continue

        zone, metrics = parts[0], parts[1]
        try:
            power_str, emission_str, count_str = metrics.split(",")
            power = float(power_str)
            emission = float(emission_str)
            count = int(count_str)
        except ValueError:
            continue

        if current_zone == zone:
            total_power += power
            total_emissions += emission
            total_count += count
        else:
            if current_zone is not None:
                avg_power = total_power / total_count if total_count > 0 else 0
                print(f"{current_zone}\t{total_count}\t{total_power:.2f}\t{avg_power:.2f}\t{total_emissions:.2f}")
            current_zone = zone
            total_power = power
            total_emissions = emission
            total_count = count

    # Emitir el último grupo procesado
    if current_zone is not None:
        avg_power = total_power / total_count if total_count > 0 else 0
        print(f"{current_zone}\t{total_count}\t{total_power:.2f}\t{avg_power:.2f}\t{total_emissions:.2f}")

if __name__ == "__main__":
    main()
