const API_BASE_URL = "http://localhost:8000/api";

export const checkAnomaly = async (features) => {
    try {
        const response = await fetch(`${API_BASE_URL}/anomaly/check`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(features),
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error("Error checking anomaly:", error);
        throw error;
    }
};

export const getLatestAnomalies = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/anomaly/latest`);
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error("Error fetching latest anomalies:", error);
        throw error;
    }
};
