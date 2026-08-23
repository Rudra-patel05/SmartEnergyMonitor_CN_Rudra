"""
Virtual IoT Energy Meter Device.

This module defines a simulated smart energy meter that generates
realistic energy consumption readings for campus areas.

IMPORTANT: All data is SIMULATED. No physical sensors or hardware are used.

The simulator produces realistic patterns based on:
  - Time of day (operating hours vs. closed hours)
  - Day of week (weekday vs. weekend)
  - Area type (lab, classroom, library, office)
  - Occupancy levels
  - Random noise for realism
"""

import random
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple, Optional

from config import NOMINAL_VOLTAGE, VOLTAGE_VARIATION


class VirtualEnergyMeter:
    """
    Simulates a smart energy meter for one campus area.

    Each instance represents a virtual IoT device that generates
    energy consumption readings. The readings follow realistic
    patterns tied to occupancy, time of day, and area type.

    Attributes:
        device_id:      Unique device identifier (e.g., "LAB-01")
        area:           Human-readable area name (e.g., "Computer Laboratory 1")
        operating_hours: Tuple of (start_hour, end_hour) when area is open
        peak_hours:     Tuple of (start_hour, end_hour) for highest activity
        max_occupancy:  Maximum number of people in the area
        base_current:   Minimum current draw in Amperes (standby mode)
        peak_current:   Maximum current draw in Amperes (full load)
        temp_range:     Tuple of (min_temp, max_temp) in Celsius
        temp_occupied_boost: Extra temperature rise when fully occupied
    """

    def __init__(self, device_config: Dict[str, Any]) -> None:
        """
        Initialize a virtual energy meter from a configuration dictionary.

        Args:
            device_config: Dictionary containing device parameters.
                           See config.py DEVICE_CONFIGS for the expected keys.
        """
        self.device_id: str = device_config["device_id"]
        self.area: str = device_config["area"]
        self.operating_hours: Tuple[int, int] = tuple(device_config["operating_hours"])
        self.peak_hours: Tuple[int, int] = tuple(device_config["peak_hours"])
        self.max_occupancy: int = device_config["max_occupancy"]
        self.base_current: float = device_config["base_current"]
        self.peak_current: float = device_config["peak_current"]
        self.temp_range: Tuple[float, float] = tuple(device_config["temp_range"])
        self.temp_occupied_boost: float = device_config["temp_occupied_boost"]

        # Cumulative energy counter (kWh) — resets each simulation run
        self._cumulative_energy: float = 0.0

    # ------------------------------------------------------------------
    # Time-based helper methods
    # ------------------------------------------------------------------

    def _is_operating_hours(self, hour: int) -> bool:
        """Check if the given hour falls within the area's operating hours."""
        return self.operating_hours[0] <= hour < self.operating_hours[1]

    def _is_peak_hours(self, hour: int) -> bool:
        """Check if the given hour falls within peak activity hours."""
        return self.peak_hours[0] <= hour < self.peak_hours[1]

    # ------------------------------------------------------------------
    # Occupancy simulation
    # ------------------------------------------------------------------

    def _calculate_occupancy(self, hour: int, day_of_week: int) -> int:
        """
        Simulate occupancy based on time and day of the week.

        Occupancy patterns:
          - Weekends:  Minimal to zero occupancy
          - Weekdays outside operating hours: Zero
          - Weekdays during peak hours: 50-95% of max capacity
          - Weekdays during non-peak operating hours: 10-50%

        Args:
            hour:        Hour of the day (0-23)
            day_of_week: Day of the week (0=Monday, 6=Sunday)

        Returns:
            Simulated occupancy count (integer >= 0)
        """
        # Weekend: very low or zero occupancy
        if day_of_week >= 5:  # Saturday = 5, Sunday = 6
            if self._is_operating_hours(hour):
                # Some areas may have minimal weekend activity
                return random.randint(0, max(1, self.max_occupancy // 10))
            return 0

        # Weekday but outside operating hours
        if not self._is_operating_hours(hour):
            return 0

        # Weekday during peak hours: high occupancy
        if self._is_peak_hours(hour):
            occupancy_fraction = random.uniform(0.5, 0.95)
        else:
            # Operating hours but not peak: moderate occupancy
            occupancy_fraction = random.uniform(0.1, 0.5)

        occupancy = int(self.max_occupancy * occupancy_fraction)

        # Add small random noise (±2 people)
        noise = random.randint(-2, 2)
        occupancy = max(0, min(self.max_occupancy, occupancy + noise))

        return occupancy

    # ------------------------------------------------------------------
    # Electrical measurements simulation
    # ------------------------------------------------------------------

    def _calculate_voltage(self) -> float:
        """
        Simulate voltage with small realistic variations.

        Indian electrical standard: 230V AC, 50Hz.
        Typical variation is ±5V under normal conditions.

        Returns:
            Voltage in Volts (float, rounded to 1 decimal)
        """
        # Gaussian distribution centered on nominal voltage
        voltage = random.gauss(NOMINAL_VOLTAGE, VOLTAGE_VARIATION / 2)

        # Clamp to realistic range (210V – 250V)
        voltage = max(210.0, min(250.0, voltage))

        return round(voltage, 1)

    def _calculate_current(self, occupancy: int, hour: int) -> float:
        """
        Calculate current draw based on occupancy and time of day.

        Logic:
          - Closed + empty:      30-60% of base current (standby devices)
          - Open but empty:      80-150% of base current (lights on, HVAC idle)
          - Open with occupancy: Scales linearly from base to peak current
                                 based on occupancy ratio, with ±10% noise

        Args:
            occupancy: Number of people in the area
            hour:      Hour of the day (0-23)

        Returns:
            Current in Amperes (float >= 0, rounded to 2 decimals)
        """
        if occupancy == 0 and not self._is_operating_hours(hour):
            # Closed and empty — minimal standby load
            # (emergency lights, security systems, standby equipment)
            current = self.base_current * random.uniform(0.3, 0.6)

        elif occupancy == 0 and self._is_operating_hours(hour):
            # Open but temporarily empty (between classes, lunch break)
            # Lights and HVAC may still be running
            current = self.base_current * random.uniform(0.8, 1.5)

        else:
            # Active usage — current scales with occupancy
            # More people → more devices active → higher current
            occupancy_ratio = occupancy / self.max_occupancy
            current_range = self.peak_current - self.base_current
            current = self.base_current + (current_range * occupancy_ratio)

            # Add ±10% noise for realism (power fluctuations, device cycling)
            noise_factor = random.uniform(0.90, 1.10)
            current *= noise_factor

        return max(0.0, round(current, 2))

    # ------------------------------------------------------------------
    # Temperature simulation
    # ------------------------------------------------------------------

    def _calculate_temperature(self, occupancy: int, hour: int) -> float:
        """
        Simulate room temperature based on occupancy and time.

        Factors:
          - Base temperature from area's configured range
          - Afternoon hours tend to be warmer (solar heating)
          - Higher occupancy increases temperature (body heat, device heat)
          - AC tries to compensate but cannot fully counteract high loads

        Args:
            occupancy: Number of people in the area
            hour:      Hour of the day (0-23)

        Returns:
            Temperature in degrees Celsius (float, rounded to 1 decimal)
        """
        base_temp = self.temp_range[0]
        temp_span = self.temp_range[1] - self.temp_range[0]

        # Time-based component: warmer in the afternoon
        if 12 <= hour <= 16:
            time_factor = 0.6
        elif 9 <= hour <= 18:
            time_factor = 0.3
        else:
            time_factor = 0.1  # Cooler at night

        # Occupancy-based component: more people → warmer
        if self.max_occupancy > 0:
            occupancy_factor = (occupancy / self.max_occupancy) * self.temp_occupied_boost
        else:
            occupancy_factor = 0.0

        temperature = base_temp + (temp_span * time_factor) + occupancy_factor

        # Add small random noise (±0.5°C)
        temperature += random.uniform(-0.5, 0.5)

        return round(temperature, 1)

    # ------------------------------------------------------------------
    # Reading generation
    # ------------------------------------------------------------------

    def generate_reading(self, timestamp: datetime, interval_seconds: int) -> Dict[str, Any]:
        """
        Generate a single energy reading for the given timestamp.

        Calculates all simulated sensor values and returns them as a dictionary.

        Power calculation:
            power_watts = voltage × current

        Energy calculation:
            energy_kwh = power_watts × (interval_seconds / 3600) / 1000
            This gives the energy consumed during the interval in kilowatt-hours.

        Args:
            timestamp:        The time of the reading
            interval_seconds: Seconds between readings (for energy calculation)

        Returns:
            Dictionary with keys: device_id, area, timestamp, voltage,
            current, power, energy, temperature, occupancy
        """
        hour = timestamp.hour
        day_of_week = timestamp.weekday()  # 0=Monday, 6=Sunday

        # Step 1: Determine occupancy for this time
        occupancy = self._calculate_occupancy(hour, day_of_week)

        # Step 2: Simulate electrical measurements
        voltage = self._calculate_voltage()
        current = self._calculate_current(occupancy, hour)

        # Step 3: Calculate power (Watts) = Voltage (V) × Current (A)
        power_watts = round(voltage * current, 2)

        # Step 4: Calculate energy consumed in this interval (kWh)
        # Formula: energy = power × time
        #   power in Watts, time in hours → result in Watt-hours
        #   divide by 1000 to convert to kilowatt-hours (kWh)
        interval_hours = interval_seconds / 3600.0
        energy_kwh = round(power_watts * interval_hours / 1000.0, 4)

        # Step 5: Accumulate total energy for this device
        self._cumulative_energy += energy_kwh

        # Step 6: Simulate temperature
        temperature = self._calculate_temperature(occupancy, hour)

        return {
            "device_id": self.device_id,
            "area": self.area,
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "voltage": voltage,
            "current": current,
            "power": power_watts,
            "energy": round(self._cumulative_energy, 4),
            "temperature": temperature,
            "occupancy": occupancy,
        }

    def generate_readings(
        self,
        num_readings: int,
        interval_seconds: int,
        start_time: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple sequential energy readings over time.

        Readings are generated at fixed intervals starting from start_time.
        If start_time is not provided, it defaults to (num_readings × interval)
        seconds ago, so the readings cover up to the current time.

        Args:
            num_readings:    Number of readings to generate
            interval_seconds: Seconds between consecutive readings
            start_time:      Starting timestamp (defaults to calculated past time)

        Returns:
            List of energy reading dictionaries in chronological order
        """
        if start_time is None:
            # Start from the past so readings end near the current time
            total_duration = num_readings * interval_seconds
            start_time = datetime.now() - timedelta(seconds=total_duration)

        # Reset cumulative energy for a fresh simulation run
        self._cumulative_energy = 0.0

        readings: List[Dict[str, Any]] = []
        current_time = start_time

        for i in range(num_readings):
            reading = self.generate_reading(current_time, interval_seconds)
            readings.append(reading)
            current_time += timedelta(seconds=interval_seconds)

        return readings

    def __repr__(self) -> str:
        return f"VirtualEnergyMeter(id={self.device_id}, area={self.area})"
