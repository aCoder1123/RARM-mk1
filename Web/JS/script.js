let speed = 1.0
let working = false

console.log('starting')


let radius

const setRadius = nRadius => radius = nRadius

// webiopi().callMacro('getRadius', [], setRadius)

radius = 10

let position = [0, 0, 0]

console.log('CONTINUING')


const statusUpdate = status => {

	let span = document.createElement('span')
	if (status[0].toLowerCase() === "e") {
		span.class = 'error'

	} else {
		span.class = "response"
	}

	span.innerText = status
	
	working = false
}

const submitMove = () => {
	if (working) return
	working = true
	webiopi().callMacro('moveToPosition', [], statusUpdate)
	
	let span = document.createElement('span')
	span.class = 'util'
	span.innerText = 'Move submitted ...'
	document.getElementById('errorsWrap').append(span)
}

const speedSubmit = () => {
	if (working) return
	working = true
	webiopi().callMacro('settingSet', ['speed', speed], statusUpdate)
	let span = document.createElement('span')
	span.class = "util"
	span.innerText = "Speed submitted ..."
	document.getElementById('errorsWrap').append(span)
	
}

const smoothingSubmit = () => {
	if (!document.getElementById('smoothingSubmit').checkValidity()) return
	working = true
	webiopi().callMacro('settingSet', ['smoothing', document.getElementById('smoothingConstantIn').value], statusUpdate)
	let span = document.createElement('span')
	span.class = 'util'
	span.innerText = 'Smoothing submitted ...'
	document.getElementById('errorsWrap').append(span)
}


document.addEventListener('keydown', e =>{
	console.log('stuff')
})

document.addEventListener('keydown', e => {
	console.log('key1')
	if (working) return
	console.log('key');

	switch (e.key) {
		case ' ':
			document.getElementById('moveSubmit').classList.add('active')
			break;
		case "ArrowUp":
			console.log('up');
			if (!(Math.sqrt(position[0]**2 + position[1]**2 + position[2]**2) < radius) && position[1] > 0) return
			position[1] +=.5
			
			document.getElementById('topBall').style.top = `${
				14 - 14 * (position[1] / radius)
			}vh`
			break;
		case "ArrowDown":
			if (
				!(
					Math.sqrt(position[0] ** 2 + position[1] ** 2 + position[2] ** 2) <
					radius
				) &&
				position[1] < 0
			)
				return
			position[1] -= 0.5
			document.getElementById('topBall').style.top = `${
				14 - 14 * (position[1] / radius)
			}vh`

			break;
		case "ArrowLeft":
			if (!(position[0] < radius)) return
			position[0] -= 0.5

			document.getElementById('topBall').style.left = `${
				14 + 14 * (position[0] / radius)
			}vh`
			break;
		case "ArrowRight":
			if (!(position[0] < radius)) return
			position[0] += 0.5

			document.getElementById('topBall').style.left = `${
				14 + 14 * (position[0] / radius)
			}vh`
			break;
		case 'w':
			position[2] += 0.5
			break;
		case 'a':
			position[2] -= 0.5
			break;
		case 's':
		
			break;
		case 'd':
			
			break;
		case 'r':
			
			break;
		case 'f':
			
			break;
		
	
		default:
			break;
	}
	console.log(position)

})

document.addEventListener('keyup', e => {
	
	if (e.key === ' ') {
		document.getElementById('moveSubmit').classList.remove('active')
		submitMove()
	}
})


