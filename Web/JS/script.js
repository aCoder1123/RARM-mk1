let speed = 1.0

const statusUpdate = status => {
	return 
}

const submitMove = () => {
	webiopi().callMacro('moveToPosition', [], statusUpdate)
}

const speedSubmit = () => {
	webiopi().callMacro('settingSet', ['speed', speed], statusUpdate)
}



document.addEventListener('keydown', e => {
	if (e.key === ' ') {
		document.getElementById('moveSubmit').classList.add('active')
	}
})

document.addEventListener('keyup', e => {
	if (e.key === ' ') {
		document.getElementById('moveSubmit').classList.remove('active')
		submitMove()
	}
})
