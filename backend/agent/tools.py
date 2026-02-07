"""Ritual State Machine for Oracle experience pacing control."""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Callable
import random
import time
import logging

logger = logging.getLogger(__name__)


class RitualState(Enum):
    """Five canonical ritual states."""
    IDLE = "IDLE"
    INVOKED = "INVOKED"
    CONTEMPLATING = "CONTEMPLATING"
    REVEALING = "REVEALING"
    COMPLETE = "COMPLETE"


class RitualStateError(Exception):
    """Invalid state transition attempted."""
    pass


VALID_TRANSITIONS: Dict[RitualState, list] = {
    RitualState.IDLE: [RitualState.INVOKED],
    RitualState.INVOKED: [RitualState.CONTEMPLATING],
    RitualState.CONTEMPLATING: [RitualState.REVEALING],
    RitualState.REVEALING: [RitualState.COMPLETE],
    RitualState.COMPLETE: [RitualState.IDLE, RitualState.INVOKED],
}

TIMING_CONFIG = {
    "contemplation_min": 1.5,
    "contemplation_max": 4.0,
    "complete_to_idle": 2.0,
    "llm_timeout": 30.0,
}


@dataclass
class RitualStateEvent:
    """Event emitted on state transitions."""
    state: RitualState
    session_id: str
    timestamp: float
    payload: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> dict:
        return {
            "state": self.state.value,
            "session_id": self.session_id,
            "timestamp": self.timestamp,
            "payload": self.payload,
        }


@dataclass
class RitualStateMachine:
    """FSM controlling oracle ritual pacing."""
    session_id: str
    current_state: RitualState = RitualState.IDLE
    state_history: list = field(default_factory=list)
    _listeners: list = field(default_factory=list)
    
    def __post_init__(self):
        self._log_transition(self.current_state, "initialized")
    
    def transition(self, new_state: RitualState, payload: Optional[dict] = None) -> RitualStateEvent:
        """Transition to new state if valid."""
        if new_state not in VALID_TRANSITIONS.get(self.current_state, []):
            raise RitualStateError(f"Invalid: {self.current_state.value} → {new_state.value}")
        
        old_state = self.current_state
        self.current_state = new_state
        
        event = RitualStateEvent(
            state=new_state,
            session_id=self.session_id,
            timestamp=time.time(),
            payload=payload,
        )
        
        self.state_history.append(event)
        self._log_transition(new_state, f"from {old_state.value}")
        self._notify_listeners(event)
        return event
    
    def get_contemplation_delay(self) -> float:
        """Get randomized contemplation delay in seconds."""
        return random.uniform(TIMING_CONFIG["contemplation_min"], TIMING_CONFIG["contemplation_max"])
    
    def force_reset(self) -> RitualStateEvent:
        """Force reset to IDLE (error recovery)."""
        logger.warning(f"[{self.session_id}] Force reset from {self.current_state.value}")
        self.current_state = RitualState.IDLE
        
        event = RitualStateEvent(
            state=RitualState.IDLE,
            session_id=self.session_id,
            timestamp=time.time(),
            payload={"forced": True},
        )
        
        self.state_history.append(event)
        self._notify_listeners(event)
        return event
    
    def add_listener(self, callback: Callable[[RitualStateEvent], None]):
        """Add listener for state transitions."""
        self._listeners.append(callback)
    
    def _notify_listeners(self, event: RitualStateEvent):
        for listener in self._listeners:
            try:
                listener(event)
            except Exception as e:
                logger.error(f"Listener error: {e}")
    
    def _log_transition(self, state: RitualState, context: str):
        logger.info(f"[{self.session_id}] State: {state.value} ({context})")
    
    def is_accepting_input(self) -> bool:
        """Check if oracle is ready for questions."""
        return self.current_state in [RitualState.IDLE, RitualState.COMPLETE]
    
    def get_state_info(self) -> dict:
        """Get current state info."""
        return {
            "current_state": self.current_state.value,
            "session_id": self.session_id,
            "accepting_input": self.is_accepting_input(),
            "history_length": len(self.state_history),
        }


_ritual_sessions: Dict[str, RitualStateMachine] = {}


def get_ritual_machine(session_id: str) -> RitualStateMachine:
    """Get or create ritual state machine for session."""
    if session_id not in _ritual_sessions:
        _ritual_sessions[session_id] = RitualStateMachine(session_id=session_id)
    return _ritual_sessions[session_id]


def clear_ritual_session(session_id: str):
    """Clear a ritual session."""
    if session_id in _ritual_sessions:
        del _ritual_sessions[session_id]


__all__ = [
    "RitualState",
    "RitualStateError",
    "RitualStateMachine",
    "RitualStateEvent",
    "TIMING_CONFIG",
    "get_ritual_machine",
    "clear_ritual_session",
]
