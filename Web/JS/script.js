let working = false

let xyzPosition = [0, 0, 24]

const statusUpdate = (macro, args, data) => {
	let span = document.createElement('span')
	// if (status[0].toLowerCase() === 'e') {
	// 	span.class = 'error'
	// } else {
	// 	span.class = 'response'
	// }

	if (data === 'Already Working') {
		span.className = 'consoleData warning'
	} else {
		working = false
		span.className = 'consoleData response'
	}

	span.innerText = macro + ': ' + data
	document.getElementById('errorsWrap').appendChild(span)
	document.getElementById('errorsWrap').scrollTop =
		document.getElementById('errorsWrap').scrollHeight
}

// const speedSubmit = () => {
// 	if (working) return
// 	working = true
// 	webiopi().callMacro('settingSet', ['speed', speed], statusUpdate)
// 	let span = document.createElement('span')
// 	span.class = 'util'
// 	span.innerText = 'Speed submitted ...'
// 	document.getElementById('errorsWrap').append(span)
// }

// const smoothingSubmit = () => {
// 	if (!document.getElementById('smoothingSubmit').checkValidity()) return
// 	working = true
// 	webiopi().callMacro(
// 		'settingSet',
// 		['smoothing', document.getElementById('smoothingConstantIn').value],
// 		statusUpdate,
// 	)
// 	let span = document.createElement('span')
// 	span.class = 'util'
// 	span.innerText = 'Smoothing submitted ...'
// 	document.getElementById('errorsWrap').append(span)
// }

document.addEventListener('keyup', e => {
	if (e.key === ' ') {
		document.getElementById('moveSubmit').classList.remove('active')
		submitMove()
	}
})

webiopi().ready(function () {
	const testLED = () => {
		if (working) {
			statusUpdate('Control', null, 'Already Working')
			return
		}
		working = true
		webiopi().callMacro('test', undefined, statusUpdate)
	}
	document.getElementById('testButton').addEventListener('click', testLED)

	submitMove = () => {
		if (working) {
			statusUpdate('Control', null, 'Already Working')
			return
		}
		working = true

		let x = Number(document.getElementById("xIn").value)
		let y = Number(document.getElementById('yIn').value)
		let z = Number(document.getElementById('zIn').value)
		xyzPosition = [x,y,z]

		if ((Math.sqrt((x**2 + y**2) + z**2)) > 24 || (Math.sqrt((x**2 + y**2) + z**2)) < 8 ){
			statusUpdate('Control', null, 'Invalid Coordinants')
			return
		}
			



		// offset =
		// 	(180 / Math.PI) * Math.atan(Math.abs(xyzPosition[0] / xyzPosition[1]))

		// theta =
		// 	xyzPosition[0] >= 0 && xyzPosition[1] >= 0
		// 		? offset
		// 		: xyzPosition[0] <= 0 && xyzPosition[1] >= 0
		// 		? offset + 90
		// 		: xyzPosition[0] <= 0 && xyzPosition[1] <= 0
		// 		? offset + 180
		// 		: offset + 270
		theta = 0
		radius = Math.sqrt(xyzPosition[0] ** 2 + xyzPosition[1] ** 2)
		TRHPosition =
			(theta) + ';' + (radius) + ';' + (xyzPosition[2])

		webiopi().callMacro('moveToPosition', [TRHPosition], statusUpdate)

		let span = document.createElement('span')
		span.className = 'consoleData util'
		span.innerText = 'Control: Move submitted'
		document.getElementById('errorsWrap').append(span)
		document.getElementById('errorsWrap').scrollTop =
			document.getElementById('errorsWrap').scrollHeight
	}
	document.getElementById('moveSubmit').addEventListener('click', submitMove)
})
