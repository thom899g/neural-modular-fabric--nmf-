"""
Neural Modular Fabric (NMF) Core Framework

This module provides a dynamic middleware framework for integrating neural modules.
It enables seamless communication, discovery, and management of neural components.

Classes:
    ModuleManager: Manages the lifecycle of neural modules.
    BrokerClient: Handles messaging between modules.
    APIService: Exposes RESTful API endpoints for NMF control.
"""

from typing import Dict, List, Optional
import logging
from functools import singledispatch
from .message_broker import MessageBroker

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class ModuleManager:
    """Manages neural modules, including discovery and lifecycle control."""
    
    def __init__(self):
        self.modules: Dict[str, object] = {}
        
    def register_module(self, module_id: str, module_class: type) -> None:
        """
        Register a new neural module.
        
        Args:
            module_id: Unique identifier for the module.
            module_class: Class of the module to instantiate.
            
        Raises:
            ValueError: If module_id already exists.
        """
        if module_id in self.modules:
            raise ValueError(f"Module {module_id} already registered.")
        try:
            instance = module_class()
            self.modules[module_id] = instance
            logger.info(f"Registered module: {module_id}")
        except Exception as e:
            logger.error(f"Failed to instantiate module {module_id}: {e}")
            raise
    
    def get_module(self, module_id: str) -> Optional[object]:
        """
        Retrieve a registered module by ID.
        
        Args:
            module_id: Unique identifier of the module.
            
        Returns:
            Module instance if found; None otherwise.
        """
        return self.modules.get(module_id)
    
class BrokerClient:
    """Manages communication between neural modules via message brokers."""
    
    def __init__(self, broker: MessageBroker):
        self.broker = broker
        
    def publish(self, topic: str, message: Dict) -> None:
        """
        Publish a message to a specific topic.
        
        Args:
            topic: Message topic name.
            message: Dictionary containing message data.
            
        Raises:
            Exception: If message publication fails.
        """
        try:
            self.broker.publish(topic, message)
            logger.info(f"Published message to {topic}")
        except Exception as e:
            logger.error(f"Failed to publish message to {topic}: {e}")
            raise
    
    def subscribe(self, topic: str, handler: callable) -> None:
        """
        Subscribe to a topic with a message handler.
        
        Args:
            topic: Topic to subscribe to.
            handler: Function to call when messages are received.
        """
        self.broker.subscribe(topic, handler)
    
class APIService:
    """Provides RESTful API for NMF control."""
    
    def __init__(self, module_manager: ModuleManager):
        self.module_manager = module_manager
        
    def get_module_status(self) -> Dict:
        """
        Retrieve status of all registered modules.
        
        Returns:
            Dictionary mapping module IDs to their statuses.
        """
        return {
            mid: "REGISTERED" if mod else "NOT REGISTERED"
            for mid, mod in self.module_manager.modules.items()
        }
    
    def register_module(self, module_id: str) -> Dict:
        """
        Register a new neural module via API.
        
        Args:
            module_id: Unique identifier of the module.
            
        Returns:
            Success message with module ID.
            
        Raises:
            ValueError: If module_id already exists.
        """
        try:
            # Mock registration logic (replace with actual module loading)
            self.module_manager.register_module(module_id, SomeModuleClass)
            return {"status": "success", "message": f"Module {module_id} registered."}
        except Exception as e:
            logger.error(f"Failed to register module {module_id}: {e}")
            raise