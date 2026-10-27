import csv
import random
from datetime import datetime, timedelta

def generate_energy_data(filename="dataset/smart_grid_energy_data.csv", num_records=100000):
    print(f"Generando dataset de {num_records} registros de telemetría de medidores inteligentes...")
    
    zones = ["Zona_Norte", "Zona_Sur", "Zona_Este", "Zona_Oeste", "Distrito_Industrial"]
    sectors = {
        "Zona_Norte": "Residencial",
        "Zona_Sur": "Residencial",
        "Zona_Este": "Comercial",
        "Zona_Oeste": "Comercial",
        "Distrito_Industrial": "Industrial"
    }
    
    # Parámetros base de consumo según sector (kWh)
    consumption_ranges = {
        "Residencial": (0.8, 4.5),
        "Comercial": (5.0, 25.0),
        "Industrial": (50.0, 280.0)
    }
    
    # Factor de emisión de CO2 promedio en la red eléctrica (aprox 0.42 kg CO2 por kWh)
    EMISSION_FACTOR = 0.42
    
    start_date = datetime(2026, 1, 1, 0, 0, 0)
    
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "RecordID", 
            "Timestamp", 
            "MeterID", 
            "Zone", 
            "SectorType", 
            "ActivePower_kWh", 
            "Voltage_V", 
            "CarbonEmission_kgCO2", 
            "PeakHour"
        ])
        
        for i in range(1, num_records + 1):
            current_time = start_date + timedelta(minutes=random.randint(0, 43200))
            hour = current_time.hour
            is_peak = 1 if (18 <= hour <= 23) else 0
            
            zone = random.choice(zones)
            sector = sectors[zone]
            min_c, max_c = consumption_ranges[sector]
            
            # Mayor consumo durante hora pico
            multiplier = 1.35 if is_peak else 1.0
            active_power = round(random.uniform(min_c, max_c) * multiplier, 3)
            voltage = round(random.uniform(215.0, 230.0), 1)
            carbon_emission = round(active_power * EMISSION_FACTOR, 4)
            meter_id = f"MTR-{zone[:3].upper()}-{random.randint(100, 999)}"
            
            writer.writerow([
                i,
                current_time.strftime("%Y-%m-%d %H:%M:%S"),
                meter_id,
                zone,
                sector,
                active_power,
                voltage,
                carbon_emission,
                is_peak
            ])
            
    print(f"Dataset generado exitosamente en: {filename}")

if __name__ == "__main__":
    generate_energy_data()
