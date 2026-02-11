#!/bin/bash
# Fetch all Florida parcels with BAS_STRT='03'
# API max is 2000 per request, so we need to paginate

BASE_URL="https://services9.arcgis.com/Gh9awoU677aKree0/arcgis/rest/services/Florida_Statewide_Cadastral/FeatureServer/0/query"
OUTPUT_DIR="/Users/luisgarcia/clawd/data"
OUTPUT_FILE="$OUTPUT_DIR/bas_strt_03_all.json"
FIELDS="PARCEL_ID,OWN_NAME,OWN_ADDR1,OWN_ADDR2,OWN_CITY,OWN_STATE,OWN_ZIPCD,PHY_ADDR1,PHY_ADDR2,PHY_CITY,PHY_ZIPCD,JV,LND_VAL,AV_SD,TV_SD,DOR_UC,CO_NO,LND_SQFOOT,ACT_YR_BLT,TOT_LVG_AR,S_LEGAL,TWN,RNG,SEC"

mkdir -p "$OUTPUT_DIR"

# Initialize
echo '{"features":[]}' > "$OUTPUT_FILE"
OFFSET=0
BATCH_SIZE=2000
TOTAL=0

echo "Fetching BAS_STRT='03' properties from Florida Statewide Parcels..."

while true; do
    echo "Fetching batch at offset $OFFSET..."
    
    # Fetch batch
    RESPONSE=$(curl -s --max-time 120 "${BASE_URL}?where=BAS_STRT+%3D+%2703%27&outFields=${FIELDS}&resultRecordCount=${BATCH_SIZE}&resultOffset=${OFFSET}&f=json")
    
    # Check for error
    if echo "$RESPONSE" | jq -e '.error' > /dev/null 2>&1; then
        echo "API Error: $(echo "$RESPONSE" | jq -r '.error.message')"
        break
    fi
    
    # Get count of features in this batch
    COUNT=$(echo "$RESPONSE" | jq '.features | length')
    
    if [ "$COUNT" -eq 0 ]; then
        echo "No more records."
        break
    fi
    
    TOTAL=$((TOTAL + COUNT))
    echo "Got $COUNT records (total: $TOTAL)"
    
    # Save batch to temp file
    echo "$RESPONSE" | jq '.features' > "/tmp/batch_${OFFSET}.json"
    
    # Check if there are more
    EXCEEDED=$(echo "$RESPONSE" | jq '.exceededTransferLimit // false')
    
    OFFSET=$((OFFSET + BATCH_SIZE))
    
    if [ "$EXCEEDED" != "true" ]; then
        echo "All records fetched."
        break
    fi
    
    # Be nice to the API
    sleep 1
done

# Combine all batches
echo "Combining batches..."
jq -s 'add' /tmp/batch_*.json > "$OUTPUT_DIR/bas_strt_03_features.json"

# Create summary
echo "Creating summary..."
jq -r '.[] | [.attributes.PARCEL_ID, .attributes.OWN_NAME, .attributes.OWN_ADDR1, .attributes.OWN_CITY, .attributes.OWN_STATE, .attributes.OWN_ZIPCD, .attributes.PHY_ADDR1, .attributes.PHY_CITY, .attributes.JV, .attributes.LND_VAL, .attributes.DOR_UC, .attributes.CO_NO] | @csv' "$OUTPUT_DIR/bas_strt_03_features.json" > "$OUTPUT_DIR/bas_strt_03.csv"

# Add header
sed -i '' '1i\
PARCEL_ID,OWN_NAME,OWN_ADDR1,OWN_CITY,OWN_STATE,OWN_ZIPCD,PHY_ADDR1,PHY_CITY,JV,LND_VAL,DOR_UC,CO_NO
' "$OUTPUT_DIR/bas_strt_03.csv"

echo ""
echo "Done! Total records: $TOTAL"
echo "JSON saved to: $OUTPUT_DIR/bas_strt_03_features.json"
echo "CSV saved to: $OUTPUT_DIR/bas_strt_03.csv"

# Cleanup temp files
rm -f /tmp/batch_*.json
