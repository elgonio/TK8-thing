function writeFile(filePath,data)
    if (type(data)=='string') then
       local file = assert(io.open(filePath,'a'),'io.open failed!'); -- create files if does not exists and appends to it;
       file:write(data);
       file:close();
       return true
    end
    return false
 end
 
 local process = openProcess('Polaris-Win64-Shipping')
for i = 0, 100 do
    pause()
    -- Create a memory scanner
    local memscan = createMemScan(process)
    
    -- Set the scan options
    memscan.firstScan(soExactValue, vtString, nil, '{"replayDetailList":', '', 0, 0xffffffffffffffff, '', fsmNotAligned, '', false, false, false, true)
    
    -- Wait for the scan to complete
    memscan.waitTillDone()
    
    local foundlist = createFoundList(memscan)
    foundlist.initialize()
    for i = 0, foundlist.getCount() - 1 do
        -- Get the address of the result
        local address = foundlist.getAddress(i)
    
        -- Read the string from memory
        local result = readString(address, 2000000)  -- Read up to 50 characters
    
        -- Print the result
        -- print('-----')
        -- print('Found at address')
        -- print(address)
        -- print(result)
    
        writeFile('D:/coding stuff/CE/data/' .. os.time() ..'_' .. i ..'.json', result)
    end
    unpause()
    sleep(120000)

end