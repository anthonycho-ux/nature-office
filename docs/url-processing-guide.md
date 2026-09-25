# URL Processing Guide for nature-office Vehicle Assessment

This guide explains how to wire a vehicle listing URL (such as an AutoTrader listing) to the agy CLI tool for processing vehicle data within the nature-office project's Windows 11 Docker environment.

## Overview

The nature-office project uses the agy CLI tool (Antigravity) for AI-powered vehicle assessments. This guide shows how to extract data from vehicle listing URLs and feed it into the 5-pillar certification system.

## Prerequisites

1. **Docker Environment**: Windows 11 VM running via dockurr/windows:6.05
2. **CLI Tools**: 
   - agy CLI (`/home/acho/.local/bin/agy`)
   - herdr (for pane management)
   - curl (for downloading URL content)
3. **Network Access**: 
   - SSH access to Windows VM on port 2222
   - HTTP access to dockurr noVNC interface on port 8006
4. **File Sharing**: Shared directories between host and Windows VM

## Step-by-Step Workflow

### 1. Prepare the Windows 11 Environment

First, ensure the Windows 11 VM is running and accessible:

```bash
# Check VM status
docker ps | grep windows-11

# Verify SSH access (may require agent user setup)
ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no -p 2222 agent@127.0.0.1 "echo 'VM ready'"
```

If SSH isn't configured, use the noVNC interface at http://127.0.0.1:8006 or run commands via herdr panes.

### 2. Download URL Content

Use curl to fetch the vehicle listing page:

```bash
# Create temporary directory for processing
mkdir -p /tmp/vehicle-processing
cd /tmp/vehicle-processing

# Fetch the AutoTrader listing (example URL)
curl -s -L \
  -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  --max-time 30 \
  "https://www.autotrader.ca/offers/ford-transit-t-250-awd-3-5l-v-6-148wb-medium-roof-w-bluetooth-gasoline-white-cat_ma29gr2160va2841tr480243-c35199e4-a604-4ab0-b48e-362c64a8ce7f" \
  -o autotrader_listing.html
```

### 3. Extract Vehicle Data Using agy

Process the HTML content with agy to extract structured vehicle data:

```bash
# Extract key vehicle specifications using agy's print mode
VEHICLE_DATA=$(agy --print='Extract the following vehicle specifications from this HTML content and return as JSON:
- Make
- Model
- Year
- Trim/Package
- Engine details
- Fuel type
- Drivetrain
- Exterior color
- Interior color
- Key features (especially those related to office conversion: solar panels, battery systems, workspace features, etc.)
- Price
- VIN (if visible)
- Mileage

Return ONLY a valid JSON object with these fields. If a field is not found, use null.

HTML CONTENT:
'"$(cat autotrader_listing_html | head -5000)"' \
  --model gemini-3.8-flash-high \
  --output-format json \
  --json-schema '{
    "type": "object",
    "properties": {
      "make": {"type": ["string", "null"]},
      "model": {"type": ["string", "null"]},
      "year": {"type": ["integer", "null"]},
      "trim": {"type": ["string", "null"]},
      "engine": {"type": ["string", "null"]},
      "fuel_type": {"type": ["string", "null"]},
      "drivetrain": {"type": ["string", "null"]},
      "exterior_color": {"type": ["string", "null"]},
      "interior_color": {"type": ["string", "null"]},
      "key_features": {"type": "array", "items": {"type": "string"}},
      "price": {"type": ["number", "null"]},
      "vin": {"type": ["string", "null"]},
      "mileage": {"type": ["integer", "null"]}
    }
  }' \
  2>/dev/null)
```

### 4. Transform Data for nature-office Assessment

Convert the extracted data into the format expected by nature-office's assessment system:

```bash
# Create specifications JSON for the agy_bridge
cat > vehicle_specs.json << 'EOF'
{
  "vehicle_id": "VT_AUTO_$(date +%s)",
  "url_source": "https://www.autotrader.ca/offers/ford-transit-t-250-awd-3-5l-v-6-148wb-medium-roof-w-bluetooth-gasoline-white-cat_ma29gr2160va2841tr480243-c35199e4-a604-4ab0-b48e-362c64a8ce7f",
  "assessment_type": "listing_based",
  "specifications": {
    "power_output_kw": 0,
    "battery_capacity_ah": 0,
    "inverter_watts": 0,
    "solar_array_watts": 0,
    "runtime_hours": 0,
    "internet_speed_mbps": 0,
    "has_redundant_connectivity": false,
    "has_external_antenna": false,
    "min_desks": 0,
    "client_seating": 0,
    "ergonomic_seating": false,
    "cable_management": false,
    "heating": false,
    "ac": false,
    "insulation": false,
    "dedicated_space": false,
    "privacy": false,
    "convertible_seating": false
  },
  "detected_features": [],
  "listing_data": {}
}
EOF

# Populate specifications based on agy extraction
if [ -n "$VEHICLE_DATA" ]; then
  # Extract make/model for vehicle ID
  MAKE=$(echo "$VEHICLE_DATA" | jq -r '.make // empty' | tr '[:upper:]' '[:lower:]')
  MODEL=$(echo "$VEHICLE_DATA" | jq -r '.model // empty' | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
  
  # Update vehicle ID
  VEHICLE_ID="${MAKE}_${MODEL}_$(date +%s | cut -c5-)"
  sed -i "s/\"vehicle_id\": \"VT_AUTO_[^\"]*\"/\"vehicle_id\": \"$VEHICLE_ID\"/" vehicle_specs.json
  
  # Parse detected features for office-related equipment
  FEATURES=$(echo "$VEHICLE_DATA" | jq -r '.key_features[]? // empty' 2>/dev/null || echo "")
  
  # Check for power-related features
  if echo "$FEATURES" | grep -iq "solar\|solar panel\|photovoltaic"; then
    jq '.specifications.solar_array_watts = 300' vehicle_specs.json > tmp.json && mv tmp.json vehicle_specs.json
  fi
  
  if echo "$FEATURES" | grep -iq "battery\|power bank\|auxiliary battery"; then
    jq '.specifications.battery_capacity_ah = 100' vehicle_specs.json > tmp.json && mv tmp.json vehicle_specs.json
  fi
  
  if echo "$FEATURES" | grep -iq "inverter\|power inverter"; then
    jq '.specifications.inverter_watts = 1000' vehicle_specs.json > tmp.json && mv tmp.json vehicle_specs.json
  fi
  
  # Check for workspace features
  if echo "$FEATURES" | grep -iq "desk\|workstation\|office"; then
    jq '.specifications.min_desks = 1' vehicle_specs.json > tmp.json && mv tmp.json vehicle_specs.json
    jq '.specifications.ergonomic_seating = true' vehicle_specs.json > tmp.json && mv tmp.json vehicle_specs.json
  fi
  
  # Check for climate features
  if echo "$FEATURES" | grep -iq "heater\|heating\|heat pump"; then
    jq '.specifications.heating = true' vehicle_specs.json > tmp.json && mv tmp.json vehicle_specs.json
  fi
  
  if echo "$FEATURES" | grep -iq "air condition\|ac\|air conditioning"; then
    jq '.specifications.ac = true' vehicle_specs.json > tmp.json && mv tmp.json vehicle_specs.json
  fi
  
  if echo "$FEATURES" | grep -iq "insulation\|thermal"; then
    jq '.specifications.insulation = true' vehicle_specs.json > tmp.json && mv tmp.json vehicle_specs.json
  fi
  
  # Check for rest/sleep features
  if echo "$FEATURES" | grep -iq "bed\|sleeping\|bunk\|convertible"; then
    jq '.specifications.dedicated_space = true' vehicle_specs.json > tmp.json && mv tmp.json vehicle_specs.json
    jq '.specifications.convertible_seating = true' vehicle_specs.json > tmp.json && mv tmp.json vehicle_specs.json
  fi
  
  # Store raw listing data
  jq --argjson listing "$VEHICLE_DATA" '.listing_data = $listing' vehicle_specs.json > tmp.json && mv tmp.json vehicle_specs.json
  
  echo "Specifications file created: vehicle_specs.json"
  cat vehicle_specs.json | jq .
fi
```

### 5. Run Vehicle Assessment via nature-office CLI

Use the nature-office CLI to perform the actual assessment:

```bash
# Navigate to nature-office project
cd /home/acho/Projects/nature-office

# Run assessment using extracted specs (without photos for listing-only assessment)
python tooling/scripts/agy_cli.py assess \
  --vehicle-id "$VEHICLE_ID" \
  --specs "$(cat /tmp/vehicle-processing/vehicle_specs.json | jq -c '.specifications')" \
  --photos ""  # Empty since we're assessing from listing data only
```

### 6. Alternative: Direct agy_bridge Usage

For more direct control, use the agy_bridge module programmatically:

```python
# Python script for direct assessment
from core.agy_bridge import AgyBridge
from core.policy import OfficeReadyPolicy
import json

def assess_from_url(url):
    # Fetch and process URL (as shown in steps 2-3 above)
    # ... processing code ...
    
    # Initialize bridge
    policy = OfficeReadyPolicy()
    bridge = AgyBridge(policy)
    
    # Perform assessment
    result = bridge.assess_vehicle(
        vehicle_id=vehicle_id,
        photos=[],  # No photos for URL-only assessment
        specs=specs_dict
    )
    
    return result

# Usage
if __name__ == "__main__":
    result = assess_from_url("https://www.autotrader.ca/offers/...")
    print(json.dumps(result, indent=2))
```

## File Sharing Considerations

### Host ↔ Windows VM Sharing

The Windows 11 VM has shared directories configured:

- **Host Path**: `/home/acho/VMs/windows-dockur/shared/`
- **VM Path**: `C:\shared\` or `/shared\` (depending on shell)
- **Host Path**: `/home/acho/VMs/windows-dockur/storage/`
- **VM Path**: `C:\storage\`

Use these for transferring larger files like vehicle photos:

```bash
# Copy photos to shared directory for VM access
cp /path/to/vehicle_photos/* /home/acho/VMs/windows-dockur/shared/

# Access from Windows VM via:
# C:\shared\vehicle_photos\
```

### Data Persistence

- **Temporary processing**: Use `/tmp/` on host for intermediate files
- **Persistent storage**: Use nature-office project directory or shared folders
- **Configuration**: Store API keys and credentials in environment variables or `.env` files

## Preprocessing Steps

### 1. URL Validation
```bash
# Basic URL validation
if [[ ! "$URL" =~ ^https?:// ]]; then
  echo "Error: Invalid URL format"
  exit 1
fi
```

### 2. Content Extraction Optimization
- Limit HTML size to prevent token overflow (first 5000-10000 chars usually sufficient)
- Remove scripts, styles, and navigation elements if possible
- Focus on main content areas (vehicle specifications sections)

### 3. Feature Mapping Table
Create a mapping between common listing features and nature-office pillars:

| Listing Feature | Power Pillar | Connectivity Pillar | Workspace Pillar | Climate Pillar | Rest Pillar |
|----------------|--------------|---------------------|------------------|----------------|-------------|
| Solar panels | ✓ | | | | |
| Auxiliary battery | ✓ | | | | |
| Power inverter | ✓ | | | | |
| 5G hotspot | | ✓ | | | |
| Satellite internet | | ✓ | | | |
| External antenna | | ✓ | | | |
| Built-in desk | | | ✓ | | |
| Ergonomic seat | | | ✓ | | |
| Cabinets/storage | | | ✓ | | |
| HVAC system | | | | ✓ | |
| Auxiliary heater | | | | ✓ | |
| Roof insulation | | | | ✓ | |
| Sleeping area | | | | | ✓ |
| Convertible seating | | | | | ✓ |
| Privacy curtains | | | | | ✓ |

### 4. Confidence Scoring
Add confidence levels to extracted data:

```json
{
  "specifications": {
    "solar_array_watts": {
      "value": 300,
      "confidence": 0.8,
      "source": "listing mentions 'solar panel kit'"
    }
  }
}
```

## Integration with 5-Pillar Certification System

The extracted data feeds directly into nature-office's assessment pipeline:

1. **Visual Assessment**: Normally done via photo analysis (skipped for URL-only)
2. **Technical Validation**: Uses specs from URL extraction
3. **Synthesis**: Combines both for final scoring

### Score Calculation Example

Based on extracted specifications, the system calculates pillar scores:

- **Power**: Based on solar array watts, battery capacity, inverter rating
- **Connectivity**: Based on internet speed, redundancy, external antenna
- **Workspace**: Based on desk count, seating, ergonomics, cable management
- **Climate**: Based on heating, AC, insulation presence
- **Rest**: Based on dedicated space, privacy, convertible seating

Each pillar has a maximum score (Power:20, Connectivity:20, Workspace:25, Climate:20, Rest:15) and minimum passing score (4 points per pillar).

## Error Handling and Fallbacks

### Network Issues
```bash
# Retry mechanism for URL fetching
MAX_RETRIES=3
for i in $(seq 1 $MAX_RETRIES); do
  if curl -s -o listing.html --max-time 15 "$URL"; then
    break
  fi
  if [ $i -eq $MAX_RETRIES ]; then
    echo "Failed to fetch URL after $MAX_RETRIES attempts"
    exit 1
  fi
  sleep $((2 ** i))  # Exponential backoff
done
```

### Extraction Failures
```bash
# Fallback to default values if extraction fails
if [ -z "$VEHICLE_DATA" ] || [ "$VEHICLE_DATA" = "{}" ]; then
  echo "Warning: Could not extract vehicle data, using conservative estimates"
  # Create minimal specs assuming no office features
  cat > vehicle_specs.json << EOF
  {
    "vehicle_id": "unknown_$(date +%s)",
    "specifications": {
      "power_output_kw": 0,
      "battery_capacity_ah": 0,
      "inverter_watts": 0,
      "solar_array_watts": 0,
      "runtime_hours": 0,
      "internet_speed_mbps": 0,
      "has_redundant_connectivity": false,
      "has_external_antenna": false,
      "min_desks": 0,
      "client_seating": 0,
      "ergonomic_seating": false,
      "cable_management": false,
      "heating": false,
      "ac": false,
      "insulation": false,
      "dedicated_space": false,
      "privacy": false,
      "convertible_seating": false
    }
  }
  EOF
fi
```

### Validation
```bash
# Validate JSON output from agy
if ! echo "$VEHICLE_DATA" | jq . >/dev/null 2>&1; then
  echo "Error: Invalid JSON returned from agy"
  echo "Raw output: $VEHICLE_DATA"
  exit 1
fi
```

## Performance Optimization

### Caching
Cache frequently accessed listings to reduce redundant processing:

```bash
# Create cache directory
CACHE_DIR="$HOME/.nature-office/url_cache"
mkdir -p "$CACHE_DIR"

# Generate cache key from URL
CACHE_KEY=$(echo "$URL" | md5sum | cut -d' ' -f1)
CACHE_FILE="$CACHE_DIR/$CACHE_KEY.json"

# Use cached data if available and fresh (< 24 hours)
if [ -f "$CACHE_FILE" ] && [ $(($(date +%s) - $(stat -c %Y "$CACHE_FILE"))) -lt 86400 ]; then
  VEHICLE_DATA=$(cat "$CACHE_FILE")
else
  # Fetch and process as normal
  # ... processing code ...
  
  # Cache the result
  echo "$VEHICLE_DATA" > "$CACHE_FILE"
fi
```

### Parallel Processing
For batch processing multiple URLs:

```bash
# Process multiple URLs in parallel (limited concurrency)
MAX_CONCURRENT=4
export -f process_vehicle_url  # Assuming function defined above

printf '%s\n' "${URLS[@]}" | xargs -n1 -P$MAX_CONCURRENT bash -c 'process_vehicle_url "$0"'
```

## Security Considerations

### Input Sanitization
All data flowing into the agy_bridge should be sanitized:

```python
# In agy_bridge.py, the sanitize_input method is used:
def sanitize_input(self, text: str) -> str:
    if not text:
        return ""
    return text.replace("\x00", "").replace("\r\n", "\n")
```

### Rate Limiting
Be respectful to vehicle listing sites:

```bash
# Add delay between requests to same domain
DOMAIN=$(echo "$URL" | awk -F/ '{print $3}')
if [ -n "$LAST_DOMAIN" ] && [ "$LAST_DOMAIN" = "$DOMAIN" ]; then
  sleep 2  # 2-second delay between requests to same domain
fi
LAST_DOMAIN="$DOMAIN"
```

## Troubleshooting

### Common Issues

1. **SSH Connection Refused**
   - Ensure agent user is created in Windows VM
   - Check SSHD service is running: `Get-Service sshd` in PowerShell
   - Verify firewall allows port 2222

2. **agy Print Mode Failures**
   - Check model availability: `/home/acho/.local/bin/agy models`
   - Verify API keys are configured
   - Try simpler prompts to isolate issues

3. **JSON Parsing Errors**
   - Ensure agy returns valid JSON
   - Use `--output-format json` flag
   - Validate with jq before processing

4. **File Permission Issues**
   - Check shared directory permissions: `ls -la /home/acho/VMs/windows-dockur/shared/`
   - Ensure VM has write access to shared folders

### Diagnostic Commands
```bash
# Check agy availability
which agy && agy --version

# Check herdr pane list (if using interactive mode)
herdr pane list

# Test network connectivity to listing site
curl -s -o /dev/null -w "%{http_code}" "$URL" --max-time 10

# Check Docker container logs
docker logs windows-11 2>&1 | tail -20

# Check shared directory mount
mount | grep shared
```

## Best Practices

### 1. Modular Design
Separate concerns into distinct functions/scripts:
- URL fetching
- Data extraction
- Specification mapping
- Assessment execution

### 2. Comprehensive Logging
```bash
# Log processing steps
LOG_FILE="/tmp/nature-office-url-processing-$(date +%Y%m%d).log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "[$(date)] Starting processing for URL: $URL"
# ... processing steps ...
echo "[$(date)] Completed assessment for vehicle: $VEHICLE_ID"
```

### 3. Configuration Management
Use environment variables or config files:
```bash
# .env file example
AGY_MODEL="gemini-3.8-flash-high"
AGY_TIMEOUT=120
MAX_RETRIES=3
CACHE_TTL=86400
```

### 4. Validation Checklist
Before considering a URL-processed assessment complete:
- [ ] Vehicle ID is unique and meaningful
- [ ] All specifications have reasonable values
- [ ] Detected features are mapped to correct pillars
- [ ] Assessment result passes basic sanity checks
- [ ] Recommendations are actionable and relevant
- [ ] All sources are properly documented

## Example Complete Script

Here's a complete example script that puts it all together:

```bash
#!/bin/bash
# process_vehicle_url.sh - Complete workflow for URL-based vehicle assessment

set -euo pipefail

URL="$1"
if [ -z "$URL" ]; then
  echo "Usage: $0 <vehicle_listing_url>"
  exit 1
fi

# Configuration
WORK_DIR="/tmp/vehicle-process-$$"
MODEL="gemini-3.8-flash-high"
TIMEOUT=120

# Setup
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

# Step 1: Fetch URL content
echo "Fetching URL: $URL"
curl -s -L \
  -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  --max-time 30 \
  "$URL" \
  -o listing.html

# Step 2: Extract vehicle data using agy
echo "Extracting vehicle specifications..."
VEHICLE_DATA=$(agy --print='Extract vehicle specifications as JSON: make, model, year, trim, engine, fuel_type, drivetrain, exterior_color, interior_color, key_features (array), price, vin, mileage. Return ONLY valid JSON.' \
  --model "$MODEL" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"make":{"type":["string","null"]},"model":{"type":["string","null"]},"year":{"type":["integer","null"]},"trim":{"type":["string","null"]},"engine":{"type":["string","null"]},"fuel_type":{"type":["string","null"]},"drivetrain":{"type":["string","null"]},"exterior_color":{"type":["string","null"]},"interior_color":{"type":["string","null"]},"key_features":{"type":"array","items":{"type":"string"}},"price":{"type":["number","null"]},"vin":{"type":["string","null"]},"mileage":{"type":["integer","null"]}}}' \
  --input-format text \
  "$(cat listing.html | head -8000)" \
  2>/dev/null)

# Validate extraction
if ! echo "$VEHICLE_DATA" | jq . >/dev/null 2>&1; then
  echo "ERROR: Failed to extract valid JSON from URL content"
  echo "Raw agy output: $VEHICLE_DATA"
  exit 1
fi

# Step 3: Map to nature-office specifications
echo "Mapping to nature-office specifications..."
cat > specs.json << 'EOF'
{
  "specifications": {
    "power_output_kw": 0,
    "battery_capacity_ah": 0,
    "inverter_watts": 0,
    "solar_array_watts": 0,
    "runtime_hours": 0,
    "internet_speed_mbps": 0,
    "has_redundant_connectivity": false,
    "has_external_antenna": false,
    "min_desks": 0,
    "client_seating": 0,
    "ergonomic_seating": false,
    "cable_management": false,
    "heating": false,
    "ac": false,
    "insulation": false,
    "dedicated_space": false,
    "privacy": false,
    "convertible_seating": false
  }
}
EOF

# Apply mappings from extracted data
MAKE=$(echo "$VEHICLE_DATA" | jq -r '.make // ""' | tr '[:upper:]' '[:lower:]')
MODEL_NAME=$(echo "$VEHICLE_DATA" | jq -r '.model // ""' | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
YEAR=$(echo "$VEHICLE_DATA" | jq -r '.year // 0')
VEHICLE_ID="${MAKE}_${MODEL_NAME}_${YEAR}_$(date +%s | cut -c5-)"

# Feature mapping
FEATURES=$(echo "$VEHICLE_DATA" | jq -r '.key_features[]? // ""' 2>/dev/null | tr '[:upper:]' '[:lower:]')

# Power features
if echo "$FEATURES" | grep -q "solar"; then
  jq '.specifications.solar_array_watts = 300' specs.json > tmp.json && mv tmp.json specs.json
fi
if echo "$FEATURES" | grep -q "battery\|power bank"; then
  jq '.specifications.battery_capacity_ah = 100' specs.json > tmp.json && mv tmp.json specs.json
fi
if echo "$FEATURES" | grep -q "inverter"; then
  jq '.specifications.inverter_watts = 1000' specs.json > tmp.json && mv tmp.json specs.json
fi

# Connectivity features
if echo "$FEATURES" | grep -q "5g\|lte\|hotspot"; then
  jq '.specifications.internet_speed_mbps = 50' specs.json > tmp.json && mv tmp.json specs.json
fi
if echo "$FEATURES" | grep -q "satellite\|starlink"; then
  jq '.specifications.has_redundant_connectivity = true' specs.json > tmp.json && mv tmp.json specs.json
  jq '.specifications.internet_speed_mbps = 100' specs.json > tmp.json && mv tmp.json specs.json
fi
if echo "$FEATURES" | grep -q "antenna\|external antenna"; then
  jq '.specifications.has_external_antenna = true' specs.json > tmp.json && mv tmp.json specs.json
fi

# Workspace features
if echo "$FEATURES" | grep -q "desk\|workstation\|office"; then
  jq '.specifications.min_desks = 1' specs.json > tmp.json && mv tmp.json specs.json
fi
if echo "$FEATURES" | grep -q "ergonomic\|lumbar support"; then
  jq '.specifications.ergonomic_seating = true' specs.json > tmp.json && mv tmp.json specs.json
fi
if echo "$FEATURES" | grep -q "cable management\|wire routing"; then
  jq '.specifications.cable_management = true' specs.json > tmp.json && mv tmp.json specs.json
fi

# Climate features
if echo "$FEATURES" | grep -q "heater\|heating\|heat pump"; then
  jq '.specifications.heating = true' specs.json > tmp.json && mv tmp.json specs.json
fi
if echo "$FEATURES" | grep -q "air condition\|ac\|air conditioning"; then
  jq '.specifications.ac = true' specs.json > tmp.json && mv tmp.json specs.json
fi
if echo "$FEATURES" | grep -q "insulation\|thermal"; then
  jq '.specifications.insulation = true' specs.json > tmp.json && mv tmp.json specs.json
fi

# Rest features
if echo "$FEATURES" | grep -q "bed\|sleeping\|bunk"; then
  jq '.specifications.dedicated_space = true' specs.json > tmp.json && mv tmp.json specs.json
fi
if echo "$FEATURES" | grep -q "convertible\|fold flat"; then
  jq '.specifications.convertible_seating = true' specs.json > tmp.json && mv tmp.json specs.json
fi
if echo "$FEATURES" | grep -q "privacy\|curtain\|partition"; then
  jq '.specifications.privacy = true' specs.json > tmp.json && mv tmp.json specs.json
fi

# Add metadata
jq --arg url "$URL" \
   --arg make "$MAKE" \
   --arg model "$MODEL_NAME" \
   --arg year "$YEAR" \
   '. + {vehicle_source: $url, detected_make: $make, detected_model: $model, detected_year: ($year|tonumber)}' \
   specs.json > tmp.json && mv tmp.json specs.json

# Step 4: Run nature-office assessment
echo "Running nature-office assessment..."
python /home/acho/Projects/nature-office/tooling/scripts/agy_cli.py assess \
  --vehicle-id "$VEHICLE_ID" \
  --specs "$(cat specs.json | jq -c '.specifications')" \
  --photos ""  # No photos for URL-only assessment

# Cleanup
cd /
rm -rf "$WORK_DIR"

echo "Assessment completed for vehicle: $VEHICLE_ID"
```

## Conclusion

This guide provides a complete workflow for wiring vehicle listing URLs to the nature-office assessment system via the agy CLI tool. By following these steps, you can:

1. Extract structured data from vehicle listing pages
2. Map that data to nature-office's 5-pillar certification framework
3. Run automated assessments using the existing agy infrastructure
4. Integrate results into the nature-office mobile office marketplace

The approach leverages existing Docker infrastructure, shared filesystems, and CLI tools to create a robust pipeline for processing vehicle listings at scale while maintaining compliance with the project's research and validation requirements.