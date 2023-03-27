let working = false

let xyzPosition = [0, 0, 0]

const statusUpdate = (macro, args, data) => {
	let span = document.createElement('span')
	// if (status[0].toLowerCase() === 'e') {
	// 	span.class = 'error'
	// } else {
	// 	span.class = 'response'
	// }

	console.log(command)
	console.log(args)
	console.log(data)
	span.innerText = data

	working = false
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
		console.log('testing')
		webiopi().callMacro('test', undefined, statusUpdate)
	}
	document.getElementById('testButton').addEventListener('click', testLED)

	submitMove = () => {
		if (working) return
		working = true
		offset =
			(180 / Math.PI) * Math.atan(Math.abs(xyzPosition[0] / xyzPosition[1]))

		theta =
			xyzPosition[0] >= 0 && xyzPosition[1] >= 0
				? offset
				: xyzPosition[0] <= 0 && xyzPosition[1] >= 0
				? offset + 90
				: xyzPosition[0] <= 0 && xyzPosition[1] <= 0
				? offset + 180
				: offset + 270
		radius = Math.sqrt(x ** 2 + y ** 2)
		TRHPosition = [theta, radius, xyzPosition[2]]

		webiopi().callMacro('moveToPosition', [TRHPosition], statusUpdate)

		let span = document.createElement('span')
		span.class = 'util'
		span.innerText = 'Move submitted ...'
		document.getElementById('errorsWrap').append(span)
	}
	document.getElementById('moveSubmit').addEventListener('click', submitMove)
})
