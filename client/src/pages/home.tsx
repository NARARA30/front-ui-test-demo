import { useState, useEffect, useCallback, useRef } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { 
  Loader2, 
  Play, 
  User, 
  Lock, 
  Trash2, 
  ChevronDown,
  MousePointer2,
  Clock,
  List,
  AlertTriangle,
  Code2,
  Moon,
  Sun
} from "lucide-react";
import type { ListItem } from "@shared/schema";

export default function Home() {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [dynamicLoaded, setDynamicLoaded] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loginResult, setLoginResult] = useState<string | null>(null);
  const [hoverMenuVisible, setHoverMenuVisible] = useState(false);
  const [selectedMenuItem, setSelectedMenuItem] = useState<string | null>(null);
  const [items, setItems] = useState<ListItem[]>([]);
  const [isLoadingMore, setIsLoadingMore] = useState(false);
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const pageRef = useRef(1);
  const isLoadingRef = useRef(false);

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [isDarkMode]);

  useEffect(() => {
    loadMoreItems();
  }, []);

  const loadMoreItems = useCallback(async () => {
    if (isLoadingRef.current) return;
    isLoadingRef.current = true;
    setIsLoadingMore(true);
    
    const currentPage = pageRef.current;
    
    try {
      const response = await fetch(`/api/items?page=${currentPage}&limit=10`);
      const data = await response.json();
      
      setItems(prev => [...prev, ...data.items]);
      pageRef.current = currentPage + 1;
    } catch (error) {
      console.error("Failed to load items:", error);
    } finally {
      isLoadingRef.current = false;
      setIsLoadingMore(false);
    }
  }, []);

  const handleScroll = useCallback((e: React.UIEvent<HTMLDivElement>) => {
    const { scrollTop, scrollHeight, clientHeight } = e.currentTarget;
    if (scrollHeight - scrollTop <= clientHeight + 100 && !isLoadingRef.current) {
      loadMoreItems();
    }
  }, [loadMoreItems]);

  const handleLoadDynamicElements = () => {
    setIsLoading(true);
    setDynamicLoaded(false);
    setTimeout(() => {
      setDynamicLoaded(true);
      setIsLoading(false);
    }, 2000);
  };

  const handleLogin = () => {
    if (username && password) {
      setLoginResult(`Login successful! User: ${username}`);
    } else {
      setLoginResult("Please enter both username and password");
    }
  };

  const handleDelete = () => {
    if (window.confirm("Are you sure you want to delete this item? This action cannot be undone.")) {
      alert("Item deleted successfully!");
    }
  };

  const handleMenuItemClick = (item: string) => {
    setSelectedMenuItem(item);
    setHoverMenuVisible(false);
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-50 border-b bg-card/80 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between gap-4 flex-wrap">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary rounded-md">
              <Code2 className="h-5 w-5 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-lg font-semibold" data-testid="text-page-title">Selenium Practice Lab</h1>
              <p className="text-sm text-muted-foreground">React + Selenium Test Automation</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="secondary" data-testid="badge-status">
              Practice Environment
            </Badge>
            <Button 
              size="icon" 
              variant="ghost" 
              onClick={() => setIsDarkMode(!isDarkMode)}
              data-testid="button-theme-toggle"
            >
              {isDarkMode ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
            </Button>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="grid gap-6 lg:grid-cols-2">
          <Card data-testid="card-dynamic-loading">
            <CardHeader>
              <div className="flex items-center gap-2">
                <Clock className="h-5 w-5 text-primary" />
                <CardTitle className="text-lg">Dynamic Element Loading</CardTitle>
              </div>
              <CardDescription>
                Test Wait strategies - Elements appear after 2 second delay
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Button 
                onClick={handleLoadDynamicElements}
                disabled={isLoading}
                className="w-full"
                data-testid="button-load-elements"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Loading...
                  </>
                ) : (
                  <>
                    <Play className="mr-2 h-4 w-4" />
                    Load Dynamic Elements
                  </>
                )}
              </Button>

              {dynamicLoaded && (
                <div 
                  className="space-y-3 p-4 bg-accent/50 rounded-md border animate-in fade-in slide-in-from-top-2 duration-300"
                  data-testid="container-dynamic-elements"
                >
                  <p className="text-sm font-medium text-foreground" data-testid="text-dynamic-message">
                    Dynamic elements loaded successfully!
                  </p>
                  <Input 
                    id="dynamic-input"
                    placeholder="This input appeared after delay"
                    data-testid="input-dynamic"
                    data-element-type="delayed-input"
                    className="selenium-dynamic-input"
                  />
                  <Button 
                    variant="secondary"
                    id="dynamic-button"
                    data-testid="button-dynamic-action"
                    data-element-type="delayed-button"
                    className="selenium-dynamic-button"
                  >
                    Dynamic Action Button
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>

          <Card data-testid="card-state-controlled-form">
            <CardHeader>
              <div className="flex items-center gap-2">
                <User className="h-5 w-5 text-primary" />
                <CardTitle className="text-lg">State-Controlled Login Form</CardTitle>
              </div>
              <CardDescription>
                React State via onChange - Direct DOM manipulation won't work
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="username">Username</Label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="username"
                    name="username"
                    placeholder="Enter username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="pl-10"
                    data-testid="input-username"
                    data-state-controlled="true"
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="password"
                    name="password"
                    type="password"
                    placeholder="Enter password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="pl-10"
                    data-testid="input-password"
                    data-state-controlled="true"
                  />
                </div>
              </div>
              <Button 
                onClick={handleLogin}
                className="w-full"
                data-testid="button-login"
              >
                Login
              </Button>
              {loginResult && (
                <div 
                  className={`p-3 rounded-md text-sm ${
                    loginResult.includes("successful") 
                      ? "bg-green-500/10 text-green-600 dark:text-green-400 border border-green-500/20" 
                      : "bg-destructive/10 text-destructive border border-destructive/20"
                  }`}
                  data-testid="text-login-result"
                >
                  {loginResult}
                </div>
              )}
              <div className="text-xs text-muted-foreground p-2 bg-muted rounded-md">
                <strong>Current State:</strong>
                <br />
                Username: <code data-testid="text-username-state">{username || "(empty)"}</code>
                <br />
                Password: <code data-testid="text-password-state">{password ? "*".repeat(password.length) : "(empty)"}</code>
              </div>
            </CardContent>
          </Card>

          <Card data-testid="card-hover-dropdown">
            <CardHeader>
              <div className="flex items-center gap-2">
                <MousePointer2 className="h-5 w-5 text-primary" />
                <CardTitle className="text-lg">Hover Dropdown Menu</CardTitle>
              </div>
              <CardDescription>
                ActionChains practice - Menu appears only on hover
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div 
                className="relative inline-block"
                onMouseEnter={() => setHoverMenuVisible(true)}
                onMouseLeave={() => setHoverMenuVisible(false)}
              >
                <Button 
                  variant="outline"
                  className="w-full"
                  data-testid="button-hover-trigger"
                  id="hover-menu-trigger"
                >
                  <span>Hover over me</span>
                  <ChevronDown className="ml-2 h-4 w-4" />
                </Button>
                <div 
                  className={`absolute top-full left-0 mt-1 w-48 bg-popover border rounded-md shadow-lg z-10 transition-all duration-200 ${
                    hoverMenuVisible 
                      ? "opacity-100 translate-y-0 visible" 
                      : "opacity-0 -translate-y-2 invisible"
                  }`}
                  data-testid="container-hover-menu"
                  id="hover-dropdown-menu"
                >
                  {["Profile Settings", "Dashboard", "Reports", "Logout"].map((item, index) => (
                    <button
                      key={item}
                      onClick={() => handleMenuItemClick(item)}
                      className="w-full text-left px-4 py-2 text-sm hover:bg-accent transition-colors first:rounded-t-md last:rounded-b-md"
                      data-testid={`menu-item-${index}`}
                      data-menu-value={item.toLowerCase().replace(" ", "-")}
                    >
                      {item}
                    </button>
                  ))}
                </div>
              </div>
              {selectedMenuItem && (
                <div className="p-3 bg-accent/50 rounded-md text-sm" data-testid="text-selected-menu-item">
                  Selected: <strong>{selectedMenuItem}</strong>
                </div>
              )}
            </CardContent>
          </Card>

          <Card data-testid="card-alert-dialog">
            <CardHeader>
              <div className="flex items-center gap-2">
                <AlertTriangle className="h-5 w-5 text-destructive" />
                <CardTitle className="text-lg">Alert Dialog Testing</CardTitle>
              </div>
              <CardDescription>
                Browser alert() handling - Confirm/dismiss dialogs
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="p-4 bg-destructive/5 border border-destructive/20 rounded-md">
                <div className="flex items-start gap-3">
                  <div className="p-2 bg-destructive/10 rounded-md">
                    <Trash2 className="h-5 w-5 text-destructive" />
                  </div>
                  <div className="flex-1">
                    <h4 className="font-medium text-sm">Danger Zone</h4>
                    <p className="text-xs text-muted-foreground mt-1">
                      Clicking this button will trigger a confirmation dialog followed by an alert.
                    </p>
                  </div>
                </div>
              </div>
              <Button 
                variant="destructive"
                onClick={handleDelete}
                className="w-full"
                data-testid="button-delete"
                id="delete-button"
              >
                <Trash2 className="mr-2 h-4 w-4" />
                Delete Item
              </Button>
              <Button 
                variant="outline"
                onClick={() => alert("This is a simple alert message for Selenium testing!")}
                className="w-full"
                data-testid="button-simple-alert"
                id="simple-alert-button"
              >
                Show Simple Alert
              </Button>
              <Button 
                variant="secondary"
                onClick={() => {
                  const result = prompt("Enter your name:", "");
                  if (result) alert(`Hello, ${result}!`);
                }}
                className="w-full"
                data-testid="button-prompt"
                id="prompt-button"
              >
                Show Prompt Dialog
              </Button>
            </CardContent>
          </Card>

          <Card className="lg:col-span-2" data-testid="card-infinite-scroll">
            <CardHeader>
              <div className="flex items-center gap-2">
                <List className="h-5 w-5 text-primary" />
                <CardTitle className="text-lg">Infinite Scroll List</CardTitle>
              </div>
              <CardDescription>
                execute_script scroll practice - More items load as you scroll or click Load More
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between gap-2 mb-4 flex-wrap">
                <div className="flex items-center gap-2">
                  <Badge variant="secondary" data-testid="badge-item-count">
                    {items.length} items loaded
                  </Badge>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={loadMoreItems}
                  disabled={isLoadingMore}
                  data-testid="button-load-more"
                >
                  {isLoadingMore ? (
                    <>
                      <Loader2 className="mr-2 h-3 w-3 animate-spin" />
                      Loading...
                    </>
                  ) : (
                    "Load More"
                  )}
                </Button>
              </div>
              <div 
                ref={scrollContainerRef}
                onScroll={handleScroll}
                className="h-80 overflow-y-auto border rounded-md"
                data-testid="container-scroll-list"
                id="infinite-scroll-container"
              >
                <div className="divide-y">
                  {items.map((item) => (
                    <div 
                      key={item.id}
                      className="p-4 hover:bg-accent/50 transition-colors"
                      data-testid={`list-item-${item.id}`}
                      data-item-id={item.id}
                    >
                      <div className="flex items-center justify-between gap-4 flex-wrap">
                        <div>
                          <h4 className="font-medium text-sm" data-testid={`item-title-${item.id}`}>
                            {item.title}
                          </h4>
                          <p className="text-xs text-muted-foreground mt-1" data-testid={`item-desc-${item.id}`}>
                            {item.description}
                          </p>
                        </div>
                        <Badge variant="outline" className="shrink-0" data-testid={`item-badge-${item.id}`}>
                          ID: {item.id}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
                {isLoadingMore && (
                  <div className="p-4 flex items-center justify-center" data-testid="loader-more-items">
                    <Loader2 className="h-5 w-5 animate-spin text-primary" />
                    <span className="ml-2 text-sm text-muted-foreground">Loading more items...</span>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        <Separator className="my-8" />

        <section className="space-y-4" data-testid="section-selectors">
          <h2 className="text-xl font-semibold">CSS Selector Practice Elements</h2>
          <p className="text-muted-foreground text-sm">
            Elements with various data attributes and class structures for selector practice
          </p>
          
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <Card className="p-4">
              <div 
                className="selenium-test__element selenium-test__element--primary"
                data-testid="selector-element-1"
                data-role="primary-element"
                data-category="selector-test"
                id="unique-element-1"
              >
                <Badge>BEM Styled</Badge>
                <p className="text-xs mt-2 text-muted-foreground">Complex CSS class structure</p>
              </div>
            </Card>
            
            <Card className="p-4">
              <div 
                className="selenium-test__element selenium-test__element--secondary"
                data-testid="selector-element-2"
                data-role="secondary-element"
                data-category="selector-test"
                id="unique-element-2"
              >
                <Badge variant="secondary">Data Attributes</Badge>
                <p className="text-xs mt-2 text-muted-foreground">Multiple data-* attributes</p>
              </div>
            </Card>
            
            <Card className="p-4">
              <div 
                className="selenium-test__element selenium-test__element--tertiary"
                data-testid="selector-element-3"
                data-role="tertiary-element"
                data-category="selector-test"
                data-contains-text="This element contains specific text"
                id="unique-element-3"
              >
                <Badge variant="outline">Contains Text</Badge>
                <p className="text-xs mt-2 text-muted-foreground">Text content extraction</p>
              </div>
            </Card>
            
            <Card className="p-4">
              <Button
                variant="ghost"
                className="selenium-test__button selenium-test__button--special w-full"
                data-testid="selector-button"
                data-action="special-click"
                data-requires-js-click="true"
                id="js-click-button"
              >
                JS Click Target
              </Button>
              <p className="text-xs mt-2 text-muted-foreground text-center">execute_script click target</p>
            </Card>
          </div>
        </section>

        <Separator className="my-8" />

        <section className="space-y-4" data-testid="section-instructions">
          <h2 className="text-xl font-semibold">Selenium Test Instructions</h2>
          <div className="grid gap-4 md:grid-cols-2">
            <Card className="p-4">
              <h3 className="font-medium mb-2">Wait Strategies</h3>
              <ul className="text-sm text-muted-foreground space-y-1">
                <li>• Use WebDriverWait for dynamic element loading</li>
                <li>• Elements appear after 2 second delay</li>
                <li>• Wait for element_to_be_clickable</li>
              </ul>
            </Card>
            <Card className="p-4">
              <h3 className="font-medium mb-2">State-Controlled Inputs</h3>
              <ul className="text-sm text-muted-foreground space-y-1">
                <li>• Use send_keys() for React inputs</li>
                <li>• Direct value setting won't trigger onChange</li>
                <li>• Verify state changes in UI</li>
              </ul>
            </Card>
            <Card className="p-4">
              <h3 className="font-medium mb-2">ActionChains</h3>
              <ul className="text-sm text-muted-foreground space-y-1">
                <li>• move_to_element() for hover menus</li>
                <li>• double_click() for special actions</li>
                <li>• Chained actions for complex interactions</li>
              </ul>
            </Card>
            <Card className="p-4">
              <h3 className="font-medium mb-2">JavaScript Execution</h3>
              <ul className="text-sm text-muted-foreground space-y-1">
                <li>• execute_script() for scroll actions</li>
                <li>• Force click on hidden elements</li>
                <li>• Trigger custom events</li>
              </ul>
            </Card>
          </div>
        </section>
      </main>

      <footer className="border-t bg-card mt-8">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between gap-4 flex-wrap">
            <p className="text-sm text-muted-foreground" data-testid="text-footer">
              Selenium Practice Lab - Built with React for Test Automation Training
            </p>
            <div className="flex items-center gap-2">
              <Badge variant="outline" data-testid="badge-version">v1.0.0</Badge>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
