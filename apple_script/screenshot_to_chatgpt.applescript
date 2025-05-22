-- Step 1: Screenshot to clipboard
do shell script "screencapture -ic"

-- Step 2: Open ChatGPT
tell application "Google Chrome"
	activate
	open location "https://chat.openai.com"
end tell

-- Step 3: Wait for ChatGPT page to fully load using JS check
tell application "Google Chrome"
    set js to "document.getElementById('prompt-textarea') !== null"
    set tries to 0
    repeat
        set isReady to execute active tab of front window javascript js
        if isReady is true then exit repeat
        delay 0.1
        set tries to tries + 1
        if tries > 40 then error "Timeout Ð textarea not found"
    end repeat
	-- repeat
    --     set js to "
    --     (function() {
    --         try {
    --             const el = document.getElementById('prompt-textarea');
    --             return el ? 'FOUND' : 'NOT FOUND';
    --         } catch (e) {
    --             return 'ERROR: ' + e.toString();
    --         }
    --     })()
    --     "
	--     -- set js to "document.getElementById('prompt-textarea')"
	-- 	set isReady to execute javascript js
    --     log isReady
	-- 	if js is "true" then exit repeat
	-- 	delay 0.1
	-- end repeat
end tell
-- Step 4: Simulate paste and enter
tell application "System Events"
	tell process "Google Chrome"
		set frontmost to true
		delay 1
		keystroke "v" using {command down}
	end tell
end tell


tell application "Google Chrome"
    set js to "document.getElementById('composer-submit-button').disabled"
    set tries to 0
    repeat
        set isReady to execute active tab of front window javascript js
        if isReady is false then exit repeat
        delay 0.1
        set tries to tries + 1
        if tries > 100 then error "Timeout Ð textarea not found"
    end repeat
end tell

tell application "System Events"
	tell process "Google Chrome"
		set frontmost to true
		delay 1
		key code 36 -- Enter
	end tell
end tell