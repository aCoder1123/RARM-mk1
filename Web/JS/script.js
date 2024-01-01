let working = false

let xyzPosition = [0, 0, 24]

const drawToCanvas = angles => {
	const canvas = document.getElementById('armDisplayCanvas')

	if (canvas.getContext) {
		let points = [
			[
				(150 * Math.cos((Math.PI * angles[0]) / 180)) / 2 + 150,
				300 - (150 * Math.sin((Math.PI * angles[0]) / 180)) / 2,
			],
			[
				(150 * Math.cos((Math.PI * (angles[0] + angles[1])) / 180) +
					150 * Math.cos((Math.PI * angles[0]) / 180)) /
					2 +
					150,
				300 -
					(150 * Math.sin((Math.PI * (angles[0] + angles[1])) / 180) +
						150 * Math.sin((Math.PI * angles[0]) / 180)) /
						2,
			],
			[
				(150 * Math.cos((Math.PI * (angles[0] + angles[1] + angles[2])) / 180) +
					150 * Math.cos((Math.PI * (angles[0] + angles[1])) / 180) +
					150 * Math.cos((Math.PI * angles[0]) / 180)) /
					2 +
					150,
				300 -
					(150 *
						Math.sin((Math.PI * (angles[0] + angles[1] + angles[2])) / 180) +
						150 * Math.sin((Math.PI * (angles[0] + angles[1])) / 180) +
						150 * Math.sin((Math.PI * angles[0]) / 180)) /
						2,
			],
		]

		const ctx = canvas.getContext('2d')

		ctx.strokeStyle = 'rgb(236, 196, 250)'
		ctx.lineWidth = 3

		ctx.beginPath()
		ctx.moveTo(150, 300)
		console.log('test')

		ctx.lineTo(points[0][0], points[0][1])
		ctx.lineTo(points[1][0], points[1][1])
		ctx.lineTo(points[2][0], points[2][1])

		ctx.stroke()

		ctx.beginPath()
		ctx.arc(150, 300, 20, 0, Math.PI * 1, true)

		ctx.fillStyle = 'rgb(200, 0, 0)'

		ctx.fill()
		ctx.beginPath()
		ctx.arc(points[0][0], points[0][1], 12, 0, Math.PI * 2, true)
		ctx.fill()
		ctx.beginPath()
		ctx.arc(points[1][0], points[1][1], 12, 0, Math.PI * 2, true)
		ctx.fill()
		ctx.beginPath()
		ctx.arc(points[2][0], points[2][1], 8, 0, Math.PI * 2, true)
		ctx.fill()

		ctx.fillStyle = 'rgb(236, 196, 250)'
		ctx.font = '20px iceland'
		ctx.fillText(`${angles[0]}°`, 150 - 14, 298)
		ctx.font = '15px iceland'
		ctx.fillText(`${angles[1]}°`, points[0][0] - 10, points[0][1] + 5)

		ctx.fillText(`${angles[2]}°`, points[1][0] - 10, points[1][1] + 5)
	} else {
		canvas.innerText = 'Canvas Browser Supported'
	}
}


const statusUpdate = (macro, data) => {
	let span = document.createElement('span')
	time = new Date().toTimeString().split(' ')[0]

	if (data === 'Already Working') {
		span.className = 'consoleData warning'
	} else {
		working = false
		span.className = 'consoleData response'
	}

	span.innerText = time + ' ~' + macro + ': ' + data
	document.getElementById('errorsWrap').appendChild(span)
	document.getElementById('errorsWrap').scrollTop =
		document.getElementById('errorsWrap').scrollHeight
	if (macro == 'arm_to_position') {
		webiopi().callMacro('get_angles', [], updateAngles)
	}
}

const speedSubmit = () => {
	if (working) return
	working = true
	speedMult = Number(document.getElementById('speedIn').value)
	webiopi().callMacro('set_setting', ['speed', speedMult], statusUpdate)
	let span = document.createElement('span')
	span.class = 'util'
	span.innerText = 'Speed submitted ...'
	document.getElementById('errorsWrap').append(span)
}

const updateAngles = (angles) => {
	if (angles === -1) {
		return
	}
	document.getElementById('lAngle').innerText = angles[0]
	document.getElementById('mAngle').innerText = angles[1]
	document.getElementById('tAngle').innerText = angles[2]
	bAngle = document.getElementById('bAngle').innerText

	radius =
		Math.cos((Math.PI / 180) * angles[0]) * 150 +
		Math.cos((Math.PI / 180) * (angles[0] + angles[1])) * 150 +
		Math.cos((Math.PI / 180) * (angles[0] + angles[1] + angles[2])) * 150

	theta = bAngle

	console.log(theta)

	ball = document.getElementById('Ball')

	ball.style = `transform: translateX(${
		1 * (Math.cos((Math.PI / 180) * theta) * radius * (14 / 450))
	}vh) translateY(${
		-1 * (Math.sin((Math.PI / 180) * theta) * radius * (14 / 450))
	}vh);`
	drawToCanvas(angles)
}

const updatePeriodic = () => {
	if (working) return
	webiopi().callMacro('get_angles', [], updateAngles)
}

if (webiopi) {
	setInterval(updatePeriodic, 1000)
}

const submitMove = () => {
	if (working) {
		statusUpdate('Control', 'Already Working')
		return
	}
	working = true

	let x = Number(document.getElementById('xIn').value)
	let y = Number(document.getElementById('yIn').value)
	let z = Number(document.getElementById('zIn').value)
	xyzPosition = [x, y, z]

	if (
		Math.sqrt(x ** 2 + y ** 2 + z ** 2) > 450 ||
		Math.sqrt(x ** 2 + y ** 2 + z ** 2) < 50
	) {
		statusUpdate('Control', `Invalid Coordinants: (${x}, ${y}, ${z}`)
		return
	}

	offset = (180 / Math.PI) * Math.atan(Math.abs(y / x))

	theta =
		x >= 0 && y >= 0
			? offset
			: x <= 0 && y >= 0
			? offset + 90
			: x <= 0 && y <= 0
			? offset + 180
			: offset + 270
	// theta = 0

	console.log(theta)
	radius = Math.sqrt(x ** 2 + y ** 2)
	TRHPosition = theta + ';' + radius + ';' + z

	ball = document.getElementById('Ball')

	ball.style = `transform: translateX(${
		1 * (Math.cos((Math.PI / 180) * theta) * radius * (14 / 450))
	}vh) translateY(${
		-1 * (Math.sin((Math.PI / 180) * theta) * radius * (14 / 450))
	}vh);`

	webiopi().callMacro('move_to_pos', [TRHPosition], statusUpdate)

	let span = document.createElement('span')
	span.className = 'consoleData util'
	span.innerText = 'Control: Move submitted'
	document.getElementById('errorsWrap').append(span)
	document.getElementById('errorsWrap').scrollTop =
		document.getElementById('errorsWrap').scrollHeight
	
	setTimeout(3000, updatePeriodic())
}

document.getElementById('moveSubmit').addEventListener('click', submitMove)

const enableToggle = () => {
	button = document.getElementById('enableSubmit')
	if (button.innerText === 'Enable') {
		button.innerText = 'Disable'
		button.className = 'sButton enabled'
		webiopi.callMacro('toggle', undefined, statusUpdate)
	} else {
		button.innerText = 'Enable'
		button.className = 'sButton'
		webiopi.callMacro('toggle', undefined, statusUpdate)
	}
}

document.getElementById('enableSubmit').addEventListener('click', enableToggle)

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

	// setInterval(updatePeriodic, 1000)
})
