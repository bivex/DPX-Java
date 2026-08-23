package com.example.patterns;

import java.util.ArrayList;
import java.util.List;

// ============================================================================
// 1. SINGLETON PATTERN
// ============================================================================
class DatabaseConnectionPool {
    private static final DatabaseConnectionPool INSTANCE = new DatabaseConnectionPool();

    private DatabaseConnectionPool() {}

    public static DatabaseConnectionPool getInstance() {
        return INSTANCE;
    }
}

// ============================================================================
// 2. STRATEGY PATTERN
// ============================================================================
interface PaymentStrategy {
    void pay(int amount);
}

class CreditCardStrategy implements PaymentStrategy {
    private String cardNumber;

    public void pay(int amount) {
        System.out.println("Paid " + amount + " using Credit Card");
    }
}

class CryptoStrategy implements PaymentStrategy {
    private String walletAddress;

    public void pay(int amount) {
        System.out.println("Paid " + amount + " using Crypto");
    }
}

// ============================================================================
// 3. COMPOSITE PATTERN
// ============================================================================
interface GraphicComponent {
    void draw();
}

class DotLeaf implements GraphicComponent {
    private int x;
    private int y;

    public void draw() {
        System.out.println("Drawing Dot at (" + x + "," + y + ")");
    }
}

class CompoundGraphicComposite implements GraphicComponent {
    private List<GraphicComponent> children = new ArrayList<>();

    public void add(GraphicComponent child) {
        children.add(child);
    }

    public void draw() {
        for (GraphicComponent child : children) {
            child.draw();
        }
    }
}

// ============================================================================
// 4. ABSTRACT FACTORY PATTERN
// ============================================================================
interface GUIFactory {
    GraphicComponent createButton();
    GraphicComponent createCheckbox();
}

class DarkThemeFactory implements GUIFactory {
    public GraphicComponent createButton() {
        return new DotLeaf();
    }
    public GraphicComponent createCheckbox() {
        return new DotLeaf();
    }
}

class LightThemeFactory implements GUIFactory {
    public GraphicComponent createButton() {
        return new DotLeaf();
    }
    public GraphicComponent createCheckbox() {
        return new DotLeaf();
    }
}
