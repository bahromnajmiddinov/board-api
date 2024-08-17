import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

from .models import BoardElement


class BoardConsumer(AsyncWebsocketConsumer):
    def get_board(self):
        return self.scope['user'].boards.filter(id=self.board_id).first()
    
    async def connect(self):
        '''
        Connect to the WebSocket group for the board.
        '''
        self.board_id = self.scope['url_route']['kwargs']['board_id']
        self.board = self.get_board()
        self.user = self.scope['user']
    
        if self.board:
            self.accept()
            await self.channel_layer.group_add(self.board_id, self.channel_name)
        else:
            self.close(code=404)
        
    async def disconnect(self, close_code):
         await self.channel_layer.group_discard(self.board_id, self.channel_name)
    
    async def receive(self, text_data):
        event = json.loads(text_data)
        event['user'] = self.user
        event['board'] = self.board
        await self.channel_layer.group_send(self.board_id, event)
    
    async def object_update(self, event):
        '''
        {
            "type": "object_update",
            "data": {
                "object_id": "unique-object-id",
                "object_type": "shape",  // could be "text", "image", "line", etc.
                "position": {
                    "x": 100,
                    "y": 200
                },
                "size": {
                    "width": 50,
                    "height": 50
                },
                "style": {
                    "color": "#ff0000",
                    "border": "2px solid #000000"
                },
                "content": "Sample Text",  // only if it's a text object
                "rotation": 45,
                "metadata": {
                    "layer": 1
                }
            },
            "timestamp": "2024-08-17T10:00:00Z"
        }

        '''
        element = BoardElement.objects.filter(id=event['data']['object_id']).first()
        if element:
            element.update(
                element_type=event['data']['object_type'],
                x_position=event['data']['position']['x'],
                y_position=event['data']['position']['y'],
                created_by=event['user'],
                width=event['data']['size']['width'],
                height=event['data']['size']['height'],
                **event['data'],
            )
            event['timestamp'] = element.updated_at.isoformat()
            self.send(text_data=json.dumps(event))
    
    async def drawing_action(self, event):
        '''
        {
            "type": "drawing_action",
            "data": {
                "path": [
                    {"x": 50, "y": 50},
                    {"x": 60, "y": 60},
                    {"x": 70, "y": 70}
                ],
                "stroke": {
                    "color": "#000000",
                    "width": 2
                },
                "tool": "pen",  // or "eraser", "highlighter", etc.
                "user_id": "user-1234"
            },
            "timestamp": "2024-08-17T10:01:00Z"
        }
        '''
        pass
    
    async def user_action(self, event):
        '''
        {
            "type": "user_action",
            "data": {
                "action": "move",
                "object_id": "unique-object-id",
                "from_position": {"x": 100, "y": 100},
                "to_position": {"x": 200, "y": 200},
                "user_id": "user-1234"
            },
            "timestamp": "2024-08-17T10:02:00Z"
        }
        '''
        pass
    
    async def board_state(self, event):
        '''
        {
            "type": "board_state",
            "data": {
                "board_id": "board-5678",
                "objects": [
                    {
                        "object_id": "unique-object-id-1",
                        "object_type": "shape",
                        "position": {"x": 100, "y": 200},
                        "size": {"width": 50, "height": 50},
                        "style": {"color": "#ff0000"},
                        "rotation": 45,
                        "content": "Sample Text",
                        "metadata": {"layer": 1}
                    },
                    {
                        "object_id": "unique-object-id-2",
                        "object_type": "image",
                        "position": {"x": 300, "y": 400},
                        "size": {"width": 100, "height": 100},
                        "src": "https://example.com/image.png"
                    }
                ]
            },
            "timestamp": "2024-08-17T10:03:00Z"
        }
        '''
        pass
    
    async def user_event(self, event):
        '''
        {
            "type": "user_event",
            "data": {
                "event": "join",
                "user_id": "user-1234",
                "user_name": "John Doe",
                "board_id": "board-5678"
            },
            "timestamp": "2024-08-17T10:04:00Z"
        }
        '''
        pass
    
    async def undo_redo(self, event):
        '''
        {
            "type": "undo_redo",
            "data": {
                "action": "undo",
                "object_id": "unique-object-id",
                "user_id": "user-1234"
            },
            "timestamp": "2024-08-17T10:05:00Z"
        }
        '''
        pass
    
    async def object_delete(self, event):
        '''
        {
            "type": "object_delete",
            "data": {
                "object_id": "unique-object-id",
                "user_id": "user-1234"
            },
            "timestamp": "2024-08-17T10:06:00Z"
        }
        '''
        element = BoardElement.objects.filter(id=event['data']['object_id']).first()
        
        if element:
            element.delete()
        
        event['timestamp'] = element.created_at.isoformat()
        self.send(text_data=json.dumps(event))
    
    async def object_create(self, event):
        '''
        {
            "type": "object_create",
            "data": {
                "object_id": "unique-object-id",
                "object_type": "shape",
                "position": {"x": 100, "y": 200},
                "size": {"width": 50, "height": 50},
                "style": {"color": "#ff0000"},
                "rotation": 45,
                "content": "Sample Text",
                "metadata": {"layer": 1},
                "user_id": "user-1234"
            },
            "timestamp": "2024-08-17T10:07:00Z"
        }
        '''
        element = BoardElement.objects.create(
            element_type=event['data']['object_type'],
            board=event['board'],
            x_position=event['data']['position']['x'],
            y_position=event['data']['position']['y'],
            created_by=event['user'],
            width=event['data']['size']['width'],
            height=event['data']['size']['height'],
            **event['data'],
        )
        
        event['data']['object_id'] = str(element.id)
        event['timestamp'] = element.created_at.isoformat()
        self.send(text_data=json.dumps(event))

