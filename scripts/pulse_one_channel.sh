VMM_OF_INTEREST="2"
CHANNEL_OF_INTEREST="15"

for BOARD_ID in {0..3}; do

    DIR="board${BOARD_ID}"
    mkdir ${DIR}

    for VMM_ID in {0..7}; do

        FILE="${DIR}/channels_board${BOARD_ID}_vmm${VMM_ID}.json"

        echo "{"                                     >> ${FILE}
        echo "  \"vmm_channel_config\" : {"          >> ${FILE}
        echo "    \"board_id\"      : ${BOARD_ID},"  >> ${FILE}
        echo "    \"vmm_id\"        : ${VMM_ID},"    >> ${FILE}
        echo "    \"description\"   : \"ST SM SD\"," >> ${FILE}
        echo "    \"configuration\" : {"             >> ${FILE}

        for CH_ID in {0..63}; do
            if [[ "$VMM_ID" == "$VMM_OF_INTEREST" &&  "$CH_ID" == "$CHANNEL_OF_INTEREST" ]] ; then
                ST="1"
                SM="0"
            else
                ST="0"
                SM="1"
            fi
            echo "      \"${CH_ID}\" : \"${ST} ${SM} 0\"," >> ${FILE}
        done

        echo "    }" >> ${FILE}
        echo "  }"   >> ${FILE}
        echo "}"     >> ${FILE}
    done
done