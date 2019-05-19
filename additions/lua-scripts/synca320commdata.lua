local version = 0.01
-- synca320 com data created by Tianyu Liu 2019
-- this script is specisically designed for flightfactor a320
-- as the com standby of a320 will not be automatically synced to x-plane's com standby

if PLANE_ICAO == "A320" and AIRCRAFT_FILENAME == "A320.acf" then
    print ("FFA320 com standby sync lua script, version: " .. version .. "" )

    -- as far as I know, the startup freq of com for FFA320 is 118.00
    local actfreqfine = 0
    local actfreqcoarse = 118
    local stbyfreqfine = 0
    local stbyfreqcoarse = 118

    local actfreq = (actfreqcoarse * 100) + actfreqfine
    local stbyfreq = (stbyfreqcoarse * 100) + stbyfreqfine

    local comFinePose = 0

    -- the value read/write via UDP, x-plane native datarefs
    dataref("COM1ACT", "sim/cockpit/radios/com1_freq_hz")
    dataref("COM1STBY", "sim/cockpit/radios/com1_stdby_freq_hz", "writable")
    dataref("COM1STBYPOSFINE", "MOKNY/FFA320/Aircraft/Cockpit/RMP1/FreqInner/Position")
    dataref("COM1STBYPOSCOARSE", "MOKNY/FFA320/Aircraft/Cockpit/RMP1/FreqOuter/Position")

    -- the command managed by ffa320connector, a320 native datarefs
    -- ("COM1STBYFINEUP", "MOKNY/FFA320/COM1_STBY_FINE_UP")
    -- ("COM1STBYFINEDOWN", "MOKNY/FFA320/COM1_STBY_FINE_DOWN")
    -- also for fine

    -- begin debug code
    -- COM1STBY = COM1STBY + 5000
    COM1STBY = 12000
    -- end debug code

    function SyncFreq()
        -- first check coarse (MHz)
        if (COM1STBY / 100) - stbyfreqcoarse > 0 then
            -- which means the value in dataref is higher than the stored value, switch up
            print(stbyfreqfine)
            command_once("MOKNY/FFA320/COM1_STBY_COARSE_UP")
            stbyfreqcoarse = stbyfreqcoarse + 1
        elseif (COM1STBY / 100) - stbyfreqcoarse < 0 then
            command_once("MOKNY/FFA320/COM1_STBY_COARSE_DOWN")
            stbyfreqcoarse = stbyfreqcoarse - 1
            -- skip when equal
        end

        -- then check fine (Khz)
        -- however, the change of Khz is a bit different, will be done later.
    end

    -- do once per second
    if (COM1STBY ~= 0) and (COM1ACT ~= 0) then
        do_often("SyncFreq()")
    end
end